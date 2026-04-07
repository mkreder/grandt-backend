import json
import pulumi
import pulumi_aws as aws


def create_rds(network):
    config = pulumi.Config()
    db_password = config.require_secret("db_password")

    vpc = network["vpc"]
    private_subnets = network["private_subnets"]

    subnet_group = aws.rds.SubnetGroup("grandt-db-subnet-group",
        subnet_ids=[s.id for s in private_subnets],
    )

    db_sg = aws.ec2.SecurityGroup("rds-sg",
        vpc_id=vpc.id,
        ingress=[{"protocol": "tcp", "from_port": 5432, "to_port": 5432, "cidr_blocks": ["10.0.0.0/16"]}],
        egress=[{"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}],
    )

    cluster = aws.rds.Cluster("grandt-aurora",
        engine="aurora-postgresql",
        engine_mode="provisioned",
        database_name="grandt",
        master_username="grandt",
        master_password=db_password,
        db_subnet_group_name=subnet_group.name,
        vpc_security_group_ids=[db_sg.id],
        skip_final_snapshot=True,
        serverlessv2_scaling_configuration={
            "min_capacity": 0.5,
            "max_capacity": 2,
        },
    )

    instance = aws.rds.ClusterInstance("grandt-aurora-instance",
        cluster_identifier=cluster.id,
        instance_class="db.serverless",
        engine=cluster.engine,
        engine_version=cluster.engine_version,
    )

    return {
        "cluster": cluster,
        "instance": instance,
        "security_group": db_sg,
        "endpoint": cluster.endpoint,
        "db_name": "grandt",
        "username": "grandt",
        "password": db_password,
    }
