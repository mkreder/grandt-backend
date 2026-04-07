import pulumi
import pulumi_aws as aws


def create_apigw(alb_out):
    alb = alb_out["alb"]

    api = aws.apigatewayv2.Api("grandt-api",
        protocol_type="HTTP",
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
