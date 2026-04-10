import pulumi
from vpc import create as create_vpc
from ecr import create as create_ecr
from alb import create as create_alb
from rds import create as create_rds
from ecs import create as create_ecs
from apigw import create as create_apigw
from pipeline import create as create_pipeline

config = pulumi.Config()
db_password = config.require_secret("db_password")
secret_key = config.require_secret("secret_key")

# VPC
vpc_out = create_vpc()

# ECR
ecr_out = create_ecr()

# ALB
alb_out = create_alb(
    vpc_id=vpc_out["vpc"].id,
    public_subnet_ids=vpc_out["public_subnet_ids"],
)

# Aurora Serverless v2
rds_out = create_rds(
    vpc_id=vpc_out["vpc"].id,
    private_subnet_ids=vpc_out["private_subnet_ids"],
    vpc_cidr="10.0.0.0/16",
)

# ECS Fargate
ecs_out = create_ecs(
    vpc_id=vpc_out["vpc"].id,
    private_subnet_ids=vpc_out["private_subnet_ids"],
    ecr_repo_url=ecr_out["repo_url"],
    target_group_arn=alb_out["target_group_arn"],
    alb_sg_id=alb_out["alb_sg_id"],
    db_endpoint=rds_out["cluster_endpoint"],
    db_password=db_password,
    secret_key=secret_key,
)

# API Gateway HTTP
apigw_out = create_apigw(
    alb_listener_arn=alb_out["listener"].arn,
    alb_dns_name=alb_out["alb_dns_name"],
    private_subnet_ids=vpc_out["private_subnet_ids"],
    alb_sg_id=alb_out["alb_sg_id"],
)

# CodePipeline
pipeline_out = create_pipeline(
    ecr_repo_url=ecr_out["repo_url"],
    cluster_name=ecs_out["cluster_name"],
    service_name=ecs_out["service_name"],
)

# Outputs
pulumi.export("vpc_id", vpc_out["vpc"].id)
pulumi.export("ecr_repo_url", ecr_out["repo_url"])
pulumi.export("alb_dns_name", alb_out["alb_dns_name"])
pulumi.export("db_endpoint", rds_out["cluster_endpoint"])
pulumi.export("ecs_cluster_name", ecs_out["cluster_name"])
pulumi.export("api_gateway_url", apigw_out["api_endpoint"])
pulumi.export("codestar_connection_arn", pipeline_out["codestar_connection_arn"])
