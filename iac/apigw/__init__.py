import pulumi
import pulumi_aws as aws


def create_apigw(alb_out):
    alb = alb_out["alb"]

    api = aws.apigatewayv2.Api("grandt-api",
        protocol_type="HTTP",
        cors_configuration={
            "allow_origins": ["https://main.d31vfa09xrom3x.amplifyapp.com"],
            "allow_methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "max_age": 86400,
        },
    )

    integration = aws.apigatewayv2.Integration("core-integration",
        api_id=api.id,
        integration_type="HTTP_PROXY",
        integration_method="ANY",
        integration_uri=alb.dns_name.apply(lambda dns: f"http://{dns}/{{proxy}}"),
    )

    aws.apigatewayv2.Route("core-route",
        api_id=api.id,
        route_key="ANY /core/{proxy+}",
        target=integration.id.apply(lambda id: f"integrations/{id}"),
    )

    stage = aws.apigatewayv2.Stage("default-stage",
        api_id=api.id,
        name="$default",
        auto_deploy=True,
    )

    return {"api": api, "stage": stage}
