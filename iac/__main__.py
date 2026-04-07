import pulumi
from vpc import create_vpc

network = create_vpc()

pulumi.export("vpc_id", network["vpc"].id)
pulumi.export("public_subnet_ids", [s.id for s in network["public_subnets"]])
pulumi.export("private_subnet_ids", [s.id for s in network["private_subnets"]])
pulumi.export("nat_gateway_id", network["nat_gateway"].id)
