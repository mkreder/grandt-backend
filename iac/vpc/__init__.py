import pulumi
import pulumi_aws as aws

AZS = ["us-east-1a", "us-east-1b", "us-east-1c"]


def create_vpc():
    vpc = aws.ec2.Vpc("grandt-vpc", cidr_block="10.0.0.0/16", enable_dns_support=True, enable_dns_hostnames=True)

    igw = aws.ec2.InternetGateway("grandt-igw", vpc_id=vpc.id)

    public_rt = aws.ec2.RouteTable("public-rt", vpc_id=vpc.id)
    aws.ec2.Route("public-route", route_table_id=public_rt.id, destination_cidr_block="0.0.0.0/0", gateway_id=igw.id)

    public_subnets = []
    for i, az in enumerate(AZS):
        subnet = aws.ec2.Subnet(f"public-{i}", vpc_id=vpc.id, cidr_block=f"10.0.{i}.0/24", availability_zone=az, map_public_ip_on_launch=True)
        aws.ec2.RouteTableAssociation(f"public-rta-{i}", subnet_id=subnet.id, route_table_id=public_rt.id)
        public_subnets.append(subnet)

    eip = aws.ec2.Eip("nat-eip", domain="vpc")
    nat = aws.ec2.NatGateway("grandt-nat", subnet_id=public_subnets[0].id, allocation_id=eip.id)

    private_rt = aws.ec2.RouteTable("private-rt", vpc_id=vpc.id)
    aws.ec2.Route("private-route", route_table_id=private_rt.id, destination_cidr_block="0.0.0.0/0", nat_gateway_id=nat.id)

    private_subnets = []
    for i, az in enumerate(AZS):
        subnet = aws.ec2.Subnet(f"private-{i}", vpc_id=vpc.id, cidr_block=f"10.0.{10 + i}.0/24", availability_zone=az)
        aws.ec2.RouteTableAssociation(f"private-rta-{i}", subnet_id=subnet.id, route_table_id=private_rt.id)
        private_subnets.append(subnet)

    return {
        "vpc": vpc,
        "public_subnets": public_subnets,
        "private_subnets": private_subnets,
        "nat_gateway": nat,
    }
