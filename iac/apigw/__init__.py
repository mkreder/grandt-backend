import pulumi_aws as aws

def create(alb_listener_arn, alb_dns_name, private_subnet_ids, alb_sg_id):
    api = aws.apigatewayv2.Api("grandt-api",
        protocol_type="HTTP",
        cors_configuration={
            "allow_origins": ["*"],
            "allow_methods": ["*"],
            "allow_headers": ["*"],
        })

    vpc_link = aws.apigatewayv2.VpcLink("grandt-vpc-link",
        security_group_ids=[alb_sg_id],
        subnet_ids=private_subnet_ids)

    integration = aws.apigatewayv2.Integration("grandt-integration",
        api_id=api.id,
        integration_type="HTTP_PROXY",
        integration_method="ANY",
        integration_uri=alb_listener_arn,
        connection_type="VPC_LINK",
        connection_id=vpc_link.id)

    aws.apigatewayv2.Route("grandt-route",
        api_id=api.id,
        route_key="ANY /{proxy+}",
        target=integration.id.apply(lambda id: f"integrations/{id}"))

    aws.apigatewayv2.Stage("grandt-stage",
        api_id=api.id,
        name="$default",
        auto_deploy=True)

    return {
        "api_endpoint": api.api_endpoint,
    }
