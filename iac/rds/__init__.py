import pulumi
import pulumi_aws as aws

def create(vpc_id, private_subnet_ids, vpc_cidr):
    config = pulumi.Config()
    db_password = config.require_secret("db_password")

    sg = aws.ec2.SecurityGroup("grandt-rds-sg",
        vpc_id=vpc_id,
        ingress=[{
            "protocol": "tcp",
            "from_port": 5432,
            "to_port": 5432,
            "cidr_blocks": [vpc_cidr],
        }],
        egress=[{
            "protocol": "-1",
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        }],
        tags={"Name": "grandt-rds-sg"})

    subnet_group = aws.rds.SubnetGroup("grandt-db-subnet",
        subnet_ids=private_subnet_ids,
        tags={"Name": "grandt-db-subnet"})

    cluster = aws.rds.Cluster("grandt-db",
        engine="aurora-postgresql",
        engine_mode="provisioned",
        engine_version="16.4",
        database_name="grandt",
        master_username="grandt",
        master_password=db_password,
        db_subnet_group_name=subnet_group.name,
        vpc_security_group_ids=[sg.id],
        serverlessv2_scaling_configuration={
            "min_capacity": 0,
            "max_capacity": 1,
        },
        skip_final_snapshot=True,
        tags={"Name": "grandt-db"})

    aws.rds.ClusterInstance("grandt-db-instance",
        cluster_identifier=cluster.id,
        instance_class="db.serverless",
        engine=cluster.engine,
        engine_version=cluster.engine_version,
        tags={"Name": "grandt-db-instance"})

    return {
        "cluster_endpoint": cluster.endpoint,
        "db_sg_id": sg.id,
    }
