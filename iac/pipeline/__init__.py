import json
import pulumi
import pulumi_aws as aws

def create(ecr_repo_url, cluster_name, service_name):
    account_id = aws.get_caller_identity().account_id
    region = "us-east-1"

    # CodeStar Connection (user must validate manually in console)
    codestar = aws.codestarconnections.Connection("grandt-github",
        name="grandt-github",
        provider_type="GitHub")

    # Artifact bucket
    artifact_bucket = aws.s3.BucketV2("grandt-pipeline-artifacts")

    # CodeBuild role
    build_assume = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "codebuild.amazonaws.com"},
            "Action": "sts:AssumeRole",
        }]
    })

    build_role = aws.iam.Role("grandt-codebuild-role", assume_role_policy=build_assume)

    aws.iam.RolePolicy("grandt-codebuild-policy",
        role=build_role.id,
        policy=pulumi.Output.all(artifact_bucket.arn).apply(lambda args: json.dumps({
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "ecr:GetAuthorizationToken",
                        "ecr:BatchCheckLayerAvailability",
                        "ecr:GetDownloadUrlForLayer",
                        "ecr:BatchGetImage",
                        "ecr:PutImage",
                        "ecr:InitiateLayerUpload",
                        "ecr:UploadLayerPart",
                        "ecr:CompleteLayerUpload",
                    ],
                    "Resource": "*",
                },
                {
                    "Effect": "Allow",
                    "Action": ["logs:CreateLogGroup", "logs:CreateLogStream", "logs:PutLogEvents"],
                    "Resource": "*",
                },
                {
                    "Effect": "Allow",
                    "Action": ["s3:GetObject", "s3:PutObject", "s3:GetBucketAcl", "s3:GetBucketLocation"],
                    "Resource": [args[0], f"{args[0]}/*"],
                },
            ],
        })))

    build_project = aws.codebuild.Project("grandt-build",
        name="grandt-backend-build",
        service_role=build_role.arn,
        artifacts={"type": "CODEPIPELINE"},
        environment={
            "compute_type": "BUILD_GENERAL1_SMALL",
            "image": "aws/codebuild/amazonlinux2-x86_64-standard:5.0",
            "type": "LINUX_CONTAINER",
            "privileged_mode": True,
            "environment_variables": [
                {"name": "AWS_DEFAULT_REGION", "value": region},
                {"name": "AWS_ACCOUNT_ID", "value": account_id},
                {"name": "ECR_REPO_URI", "value": ecr_repo_url},
            ],
        },
        source={"type": "CODEPIPELINE"})

    # Pipeline role
    pipeline_assume = json.dumps({
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "codepipeline.amazonaws.com"},
            "Action": "sts:AssumeRole",
        }]
    })

    pipeline_role = aws.iam.Role("grandt-pipeline-role", assume_role_policy=pipeline_assume)

    aws.iam.RolePolicy("grandt-pipeline-policy",
        role=pipeline_role.id,
        policy=pulumi.Output.all(artifact_bucket.arn, codestar.arn, build_project.arn).apply(
            lambda args: json.dumps({
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": ["s3:GetObject", "s3:PutObject", "s3:GetBucketVersioning"],
                        "Resource": [args[0], f"{args[0]}/*"],
                    },
                    {
                        "Effect": "Allow",
                        "Action": ["codestar-connections:UseConnection"],
                        "Resource": args[1],
                    },
                    {
                        "Effect": "Allow",
                        "Action": ["codebuild:BatchGetBuilds", "codebuild:StartBuild"],
                        "Resource": args[2],
                    },
                    {
                        "Effect": "Allow",
                        "Action": [
                            "ecs:DescribeServices",
                            "ecs:DescribeTaskDefinition",
                            "ecs:DescribeTasks",
                            "ecs:ListTasks",
                            "ecs:RegisterTaskDefinition",
                            "ecs:UpdateService",
                        ],
                        "Resource": "*",
                    },
                    {
                        "Effect": "Allow",
                        "Action": "iam:PassRole",
                        "Resource": "*",
                        "Condition": {
                            "StringEqualsIfExists": {
                                "iam:PassedToService": "ecs-tasks.amazonaws.com"
                            }
                        },
                    },
                ],
            })
        ))

    aws.codepipeline.Pipeline("grandt-pipeline",
        name="grandt-backend",
        role_arn=pipeline_role.arn,
        artifact_stores=[{
            "location": artifact_bucket.bucket,
            "type": "S3",
        }],
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
                        "ConnectionArn": codestar.arn,
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
                    "configuration": {
                        "ProjectName": build_project.name,
                    },
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
                        "ClusterName": cluster_name,
                        "ServiceName": service_name,
                    },
                }],
            },
        ])

    return {
        "codestar_connection_arn": codestar.arn,
    }
