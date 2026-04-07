import pulumi_aws as aws


def create_ecr():
    repo = aws.ecr.Repository("grandt-backend",
        image_tag_mutability="MUTABLE",
        force_delete=True,
        image_scanning_configuration={"scanOnPush": True},
    )

    aws.ecr.LifecyclePolicy("grandt-backend-lifecycle",
        repository=repo.name,
        policy="""{
            "rules": [{"rulePriority": 1, "selection": {"tagStatus": "untagged", "countType": "imageCountMoreThan", "countNumber": 5}, "action": {"type": "expire"}}]
        }""",
    )

    return {"repository": repo}
