import pulumi
from vpc import create_vpc
from ecr import create_ecr
from alb import create_alb
from ecs import create_ecs
from apigw import create_apigw
from pipeline import create_pipeline
from rds import create_rds

network = create_vpc()
ecr_out = create_ecr()
alb_out = create_alb(network)
rds_out = create_rds(network)
ecs_out = create_ecs(network, ecr_out, alb_out, rds_out)
apigw_out = create_apigw(alb_out)
pipeline_out = create_pipeline(ecr_out, ecs_out)

pulumi.export("vpc_id", network["vpc"].id)
pulumi.export("ecr_repo_url", ecr_out["repository"].repository_url)
pulumi.export("alb_dns", alb_out["alb"].dns_name)
pulumi.export("api_endpoint", apigw_out["api"].api_endpoint)
pulumi.export("ecs_cluster", ecs_out["cluster"].name)
pulumi.export("github_connection_arn", pipeline_out["connection"].arn)
pulumi.export("db_endpoint", rds_out["endpoint"])
