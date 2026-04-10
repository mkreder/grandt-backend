import pulumi
import pulumi_aws as aws

def create():
    azs = ["us-east-1a", "us-east-1b", "us-east-1c"]

    vpc = aws.ec2.Vpc("grandt-vpc",
        cidr_block="10.0.0.0/16",
        enable_dns_support=True,
        enable_dns_hostnames=True,
        tags={"Name": "grandt-vpc"})

    igw = aws.ec2.InternetGateway("grandt-igw",
        vpc_id=vpc.id,
        tags={"Name": "grandt-igw"})

    # Public subnets
    public_subnets = []
    for i, az in enumerate(azs):
        subnet = aws.ec2.Subnet(f"grandt-public-{i+1}",
            vpc_id=vpc.id,
            cidr_block=f"10.0.{i+1}.0/24",
            availability_zone=az,
            map_public_ip_on_launch=True,
            tags={"Name": f"grandt-public-{i+1}"})
        public_subnets.append(subnet)

    public_rt = aws.ec2.RouteTable("grandt-public-rt",
        vpc_id=vpc.id,
        routes=[{"cidr_block": "0.0.0.0/0", "gateway_id": igw.id}],
        tags={"Name": "grandt-public-rt"})

    for i, subnet in enumerate(public_subnets):
        aws.ec2.RouteTableAssociation(f"grandt-public-rta-{i+1}",
            subnet_id=subnet.id,
            route_table_id=public_rt.id)

    # NAT Gateway
    eip = aws.ec2.Eip("grandt-nat-eip", domain="vpc")
    nat = aws.ec2.NatGateway("grandt-nat",
        subnet_id=public_subnets[0].id,
        allocation_id=eip.id,
        tags={"Name": "grandt-nat"})

    # Private subnets
    private_subnets = []
    for i, az in enumerate(azs):
        subnet = aws.ec2.Subnet(f"grandt-private-{i+1}",
            vpc_id=vpc.id,
            cidr_block=f"10.0.{101+i}.0/24",
            availability_zone=az,
            tags={"Name": f"grandt-private-{i+1}"})
        private_subnets.append(subnet)

    private_rt = aws.ec2.RouteTable("grandt-private-rt",
        vpc_id=vpc.id,
        routes=[{"cidr_block": "0.0.0.0/0", "nat_gateway_id": nat.id}],
        tags={"Name": "grandt-private-rt"})

    for i, subnet in enumerate(private_subnets):
        aws.ec2.RouteTableAssociation(f"grandt-private-rta-{i+1}",
            subnet_id=subnet.id,
            route_table_id=private_rt.id)

    return {
        "vpc": vpc,
        "public_subnet_ids": [s.id for s in public_subnets],
        "private_subnet_ids": [s.id for s in private_subnets],
    }
