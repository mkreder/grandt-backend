import pulumi_aws as aws

def create(vpc_id, public_subnet_ids):
    sg = aws.ec2.SecurityGroup("grandt-alb-sg",
        vpc_id=vpc_id,
        ingress=[{
            "protocol": "tcp",
            "from_port": 80,
            "to_port": 80,
            "cidr_blocks": ["0.0.0.0/0"],
        }],
        egress=[{
            "protocol": "-1",
            "from_port": 0,
            "to_port": 0,
            "cidr_blocks": ["0.0.0.0/0"],
        }],
        tags={"Name": "grandt-alb-sg"})

    alb = aws.lb.LoadBalancer("grandt-alb",
        internal=False,
        load_balancer_type="application",
        security_groups=[sg.id],
        subnets=public_subnet_ids,
        tags={"Name": "grandt-alb"})

    tg = aws.lb.TargetGroup("grandt-tg",
        port=8000,
        protocol="HTTP",
        target_type="ip",
        vpc_id=vpc_id,
        health_check={
            "path": "/health",
            "protocol": "HTTP",
            "interval": 30,
            "timeout": 5,
            "healthy_threshold": 2,
            "unhealthy_threshold": 3,
        },
        tags={"Name": "grandt-tg"})

    listener = aws.lb.Listener("grandt-listener",
        load_balancer_arn=alb.arn,
        port=80,
        protocol="HTTP",
        default_actions=[{
            "type": "forward",
            "target_group_arn": tg.arn,
        }])

    return {
        "alb": alb,
        "target_group_arn": tg.arn,
        "alb_sg_id": sg.id,
        "listener": listener,
        "alb_dns_name": alb.dns_name,
    }
