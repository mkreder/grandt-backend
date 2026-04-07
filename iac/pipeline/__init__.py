import json
import pulumi
import pulumi_aws as aws


def create_pipeline(ecr_out, ecs_out):
    repo = ecr_out["repository"]
    cluster = ecs_out["cluster"]
    service = ecs_out["service"]

    account_id = aws.get_caller_identity().account_id
    region = aws.get_region().name

    # Artifact bucket
    artifact_bucket = aws.s3.BucketV2("pipeline-artifacts")

    # CodeBuild role
    build_role = aws.iam.Role("codebuild-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Principal": {"Service": "codebuild.amazonaws.com"}, "Action": "sts:AssumeRole"}],
        }),
    )
    aws.iam.RolePolicy("codebuild-policy",
        role=build_role.id,
        policy=pulumi.Output.all(repo.arn, artifact_bucket.arn).apply(lambda args: json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {"Effect": "Allow", "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"], "Resource": "*"},
                {"Effect": "Allow", "Action": ["ecr:GetAuthorizationToken"], "Resource": "*"},
                {"Effect": "Allow", "Action": ["ecr:BatchCheckLayerAvailability", "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage", "ecr:PutImage", "ecr:InitiateLayerUpload", "ecr:UploadLayerPart", "ecr:CompleteLayerUpload"], "Resource": args[0]},
                {"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject", "s3:GetBucketAcl", "s3:GetBucketLocation"], "Resource": [args[1], f"{args[1]}/*"]},
            ],
        })),
    )

    # CodeBuild project
    build_project = aws.codebuild.Project("grandt-backend-build",
        service_role=build_role.arn,
        artifacts={"type": "CODEPIPELINE"},
        environment={
            "compute_type": "BUILD_GENERAL1_SMALL",
            "image": "aws/codebuild/amazonlinux2-x86_64-standard:5.0",
            "type": "LINUX_CONTAINER",
            "privileged_mode": True,
            "environment_variables": [
                {"name": "ECR_REPO_URI", "value": repo.repository_url},
                {"name": "AWS_ACCOUNT_ID", "value": account_id},
                {"name": "AWS_DEFAULT_REGION", "value": region},
            ],
        },
        source={"type": "CODEPIPELINE", "buildspec": "buildspec.yml"},
    )

    # CodePipeline role
    pipeline_role = aws.iam.Role("codepipeline-role",
        assume_role_policy=json.dumps({
            "Version": "2012-10-17",
            "Statement": [{"Effect": "Allow", "Principal": {"Service": "codepipeline.amazonaws.com"}, "Action": "sts:AssumeRole"}],
        }),
    )
    aws.iam.RolePolicy("codepipeline-policy",
        role=pipeline_role.id,
        policy=pulumi.Output.all(artifact_bucket.arn).apply(lambda args: json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {"Effect": "Allow", "Action": ["s3:GetObject", "s3:PutObject", "s3:GetBucketVersioning"], "Resource": [args[0], f"{args[0]}/*"]},
                {"Effect": "Allow", "Action": ["codebuild:BatchGetBuilds", "codebuild:StartBuild"], "Resource": "*"},
                {"Effect": "Allow", "Action": ["ecs:DescribeServices", "ecs:DescribeTaskDefinition", "ecs:DescribeTasks", "ecs:ListTasks", "ecs:RegisterTaskDefinition", "ecs:UpdateService"], "Resource": "*"},
                {"Effect": "Allow", "Action": ["iam:PassRole"], "Resource": "*", "Condition": {"StringEqualsIfExists": {"iam:PassedToService": ["ecs-tasks.amazonaws.com"]}}},
                {"Effect": "Allow", "Action": ["codestar-connections:UseConnection"], "Resource": "*"},
            ],
        })),
    )

    # Connection to GitHub (needs manual confirmation in console)
    connection = aws.codeconnections.Connection("github-connection",
        provider_type="GitHub",
    )

    # Pipeline
    pipeline = aws.codepipeline.Pipeline("grandt-backend-pipeline",
        role_arn=pipeline_role.arn,
        artifact_stores=[{"location": artifact_bucket.bucket, "type": "S3"}],
        stages=[
            {
                "name": "Source",
                "actions": [{
                    "name": "GitHub",
                    "category": "Source",
                    "owner": "AWS",
                    "provider": "CodeStarSourceConnection",
                    "version": "1",
                    "output_artifacts": ["source_output"],
                    "configuration": {
                        "ConnectionArn": connection.arn,
                        "FullRepositoryId": "mkreder/grandt-backend",
                        "BranchName": "main",
                    },
                }],
            },
            {
                "name": "Build",
                "actions": [{
                    "name": "Build",
                    "category": "Build",
                    "owner": "AWS",
                    "provider": "CodeBuild",
                    "version": "1",
                    "input_artifacts": ["source_output"],
                    "output_artifacts": ["build_output"],
                    "configuration": {"ProjectName": build_project.name},
                }],
            },
            {
                "name": "Deploy",
                "actions": [{
                    "name": "Deploy",
                    "category": "Deploy",
                    "owner": "AWS",
                    "provider": "ECS",
                    "version": "1",
                    "input_artifacts": ["build_output"],
                    "configuration": {
                        "ClusterName": cluster.name,
                        "ServiceName": service.name,
                        "FileName": "imagedefinitions.json",
                    },
                }],
            },
        ],
    )

    return {"pipeline": pipeline, "build_project": build_project, "connection": connection}
