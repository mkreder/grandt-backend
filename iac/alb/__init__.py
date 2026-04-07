import json
import pulumi
import pulumi_aws as aws


def create_alb(network):
    vpc = network["vpc"]
    public_subnets = network["public_subnets"]

    alb_sg = aws.ec2.SecurityGroup("alb-sg",
        vpc_id=vpc.id,
        ingress=[{"protocol": "tcp", "from_port": 80, "to_port": 80, "cidr_blocks": ["0.0.0.0/0"]}],
        egress=[{"protocol": "-1", "from_port": 0, "to_port": 0, "cidr_blocks": ["0.0.0.0/0"]}],
    )

    alb = aws.lb.LoadBalancer("grandt-alb",
        internal=False,
        load_balancer_type="application",
        security_groups=[alb_sg.id],
        subnets=[s.id for s in public_subnets],
    )

    tg = aws.lb.TargetGroup("grandt-backend-tg",
        port=8000,
        protocol="HTTP",
        vpc_id=vpc.id,
        target_type="ip",
        health_check={"path": "/health", "interval": 30, "healthy_threshold": 2, "unhealthy_threshold": 3},
    )

    aws.lb.Listener("grandt-http-listener",
        load_balancer_arn=alb.arn,
        port=80,
        default_actions=[{"type": "forward", "target_group_arn": tg.arn}],
    )

    return {"alb": alb, "target_group": tg, "security_group": alb_sg}
