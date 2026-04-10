import json
import pulumi_aws as aws

def create():
    repo = aws.ecr.Repository("grandt-backend",
        name="grandt-backend",
        image_tag_mutability="MUTABLE",
        force_delete=True)

    aws.ecr.LifecyclePolicy("grandt-backend-lifecycle",
        repository=repo.name,
        policy=json.dumps({
            "rules": [{
                "rulePriority": 1,
                "description": "Keep max 5 untagged images",
                "selection": {
                    "tagStatus": "untagged",
                    "countType": "imageCountMoreThan",
                    "countNumber": 5,
                },
                "action": {"type": "expire"},
            }]
        }))

    return {
        "repo_url": repo.repository_url,
        "repo_name": repo.name,
    }
