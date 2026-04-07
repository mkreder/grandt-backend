import json
import pulumi
import pulumi_aws as aws


def create_ecs(network, ecr_out, alb_out):
    vpc = network["vpc"]
    private_subnets = network["private_subnets"]
    repo = ecr_out["repository"]
    tg = alb_out["target_group"]
    alb_sg = alb_out["security_group"]

    cluster = aws.ecs.Cluster("grandt-cluster")

    task_sg = aws.ec2.SecurityGroup("ecs-task-sg",
        vpc_id=vpc.id,
        ingress=[{"protocol": "tcp", "from_port": 8000, "to_port": 8000, "security_groups": [alb_sg.id]}],
        egress=[{"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}],
    )

    exec_role = aws.iam.Role("ecs-exec-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Principal": {"Service": "ecs-tasks.amazonaws.com"}, "Action": "sts:AssumeRole"}],
        }),
    )
    aws.iam.RolePolicyAttachment("ecs-exec-policy",
        role=exec_role.name,
        policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy",
    )

    task_role = aws.iam.Role("ecs-task-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Principal": {"Service": "ecs-tasks.amazonaws.com"}, "Action": "sts:AssumeRole"}],
        }),
    )

    task_def = aws.ecs.TaskDefinition("grandt-backend-task",
        family="grandt-backend",
        cpu="256",
        memory="512",
        network_mode="awsvpc",
        requires_compatibilities=["FARGATE"],
        execution_role_arn=exec_role.arn,
        task_role_arn=task_role.arn,
        container_definitions=repo.repository_url.apply(lambda url: json.dumps([{
            "name": "backend",
            "image": f"{url}:latest",
            "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": "/ecs/grandt-backend",
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "ecs",
                    "awslogs-create-group": "true",
                },
            },
        }])),
    )

    service = aws.ecs.Service("grandt-backend-svc",
        cluster=cluster.arn,
        task_definition=task_def.arn,
        desired_count=1,
        launch_type="FARGATE",
        network_configuration={
            "subnets": [s.id for s in private_subnets],
            "security_groups": [task_sg.id],
            "assign_public_ip": False,
        },
        load_balancers=[{
            "target_group_arn": tg.arn,
            "container_name": "backend",
            "container_port": 8000,
        }],
        deployment_circuit_breaker={"enable": True, "rollback": True},
    )

    return {"cluster": cluster, "service": service, "task_definition": task_def}
