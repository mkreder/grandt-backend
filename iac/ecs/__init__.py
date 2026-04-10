import json
import pulumi
import pulumi_aws as aws

def create(vpc_id, private_subnet_ids, ecr_repo_url, target_group_arn, alb_sg_id, db_endpoint, db_password, secret_key):
    cluster = aws.ecs.Cluster("grandt-cluster", tags={"Name": "grandt-cluster"})

    assume_role_policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {"Service": "ecs-tasks.amazonaws.com"},
        }]
    })

    exec_role = aws.iam.Role("grandt-ecs-exec-role",
        assume_role_policy=assume_role_policy)

    aws.iam.RolePolicyAttachment("grandt-ecs-exec-policy",
        role=exec_role.name,
        policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy")

    task_role = aws.iam.Role("grandt-ecs-task-role",
        assume_role_policy=assume_role_policy)

    sg = aws.ec2.SecurityGroup("grandt-ecs-sg",
        vpc_id=vpc_id,
        ingress=[{
            "protocol": "tcp",
            "from_port": 8000,
            "to_port": 8000,
            "security_groups": [alb_sg_id],
        }],
        egress=[{
            "protocol": "-1",
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        }],
        tags={"Name": "grandt-ecs-sg"})

    log_group = aws.cloudwatch.LogGroup("grandt-backend-logs",
        name="/ecs/grandt-backend",
        retention_in_days=7)

    database_url = pulumi.Output.all(db_endpoint, db_password).apply(
        lambda args: f"postgresql://grandt:{args[1]}@{args[0]}:5432/grandt"
    )

    container_defs = pulumi.Output.all(ecr_repo_url, database_url, secret_key, log_group.name).apply(
        lambda args: json.dumps([{
            "name": "backend",
            "image": f"{args[0]}:latest",
            "portMappings": [{"containerPort": 8000, "protocol": "tcp"}],
            "environment": [
                {"name": "DATABASE_URL", "value": args[1]},
                {"name": "SECRET_KEY", "value": args[2]},
            ],
            "logConfiguration": {
                "logDriver": "awslogs",
                "options": {
                    "awslogs-group": args[3],
                    "awslogs-region": "us-east-1",
                    "awslogs-stream-prefix": "ecs",
                },
            },
        }])
    )

    task_def = aws.ecs.TaskDefinition("grandt-task",
        family="grandt-backend",
        cpu="256",
        memory="512",
        network_mode="awsvpc",
        requires_compatibilities=["FARGATE"],
        execution_role_arn=exec_role.arn,
        task_role_arn=task_role.arn,
        container_definitions=container_defs)

    service = aws.ecs.Service("grandt-service",
        cluster=cluster.arn,
        task_definition=task_def.arn,
        desired_count=1,
        launch_type="FARGATE",
        network_configuration={
            "subnets": private_subnet_ids,
            "security_groups": [sg.id],
            "assign_public_ip": False,
        },
        load_balancers=[{
            "target_group_arn": target_group_arn,
            "container_name": "backend",
            "container_port": 8000,
        }],
        deployment_circuit_breaker={
            "enable": True,
            "rollback": True,
        })

    return {
        "cluster_name": cluster.name,
        "service_name": service.name,
        "cluster_arn": cluster.arn,
    }
