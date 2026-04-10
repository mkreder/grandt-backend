# grandt-backend

Backend en FastAPI usado en la charla **"No todo es Kubernetes"**, donde muestro cómo levantar un servicio en AWS con **ECS Fargate + CodePipeline** (y el frontend en **Amplify**) como alternativa a Kubernetes.

Repo del frontend: [mkreder/grandt-frontend](https://github.com/mkreder/grandt-frontend)

## Stack

- **API**: FastAPI + SQLAlchemy + Alembic
- **DB**: PostgreSQL (Aurora Serverless v2 en AWS, Postgres local vía `docker-compose`)
- **Infra**: Pulumi (Python) en `iac/`
- **CI/CD**: CodePipeline + CodeBuild (`buildspec.yml`) → ECR → ECS

## Correr local

```bash
docker-compose up -d
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000
```

## Arquitectura en AWS

```
GitHub ──▶ CodePipeline ──▶ CodeBuild ──▶ ECR
                                            │
                                            ▼
        API Gateway (HTTP) ──▶ ALB ──▶ ECS Fargate ──▶ Aurora Serverless v2
                                          (VPC privada)
```

El frontend en Amplify consume la API a través de API Gateway bajo la ruta `/core/*`.

---

## Prompt usado para generar la IaC

A continuación, el prompt original que se le pasó a Claude Code para generar toda la infraestructura en `iac/`:

> Creá la infraestructura en AWS con Pulumi (Python, pulumi-aws) para deployar este backend FastAPI en ECS Fargate. Todo en `backend/iac/`, región us-east-1, profile `personal`.
>
> ### Componentes
>
> 1. **VPC**: CIDR 10.0.0.0/16, 3 subnets públicas y 3 privadas en us-east-1a/b/c, Internet Gateway, NAT Gateway.
>
> 2. **ECR**: Repositorio `grandt-backend` con lifecycle policy (max 5 imágenes untagged).
>
> 3. **ALB**: Application Load Balancer público en subnets públicas, target group port 8000 con health check en `/health`, listener HTTP:80.
>
> 4. **Aurora Serverless v2**: PostgreSQL en subnets privadas, 0-1 ACU, SG permite 5432 desde VPC CIDR.
>
> 5. **ECS Fargate**: Cluster con task definition (256 CPU, 512 MB), container `backend` en port 8000 con env vars `DATABASE_URL` (postgresql://grandt:{pass}@{aurora_endpoint}:5432/grandt) y `SECRET_KEY` (desde config secret). Service con 1 task en subnets privadas, registrado en ALB target group, circuit breaker con rollback.
>
> 6. **API Gateway HTTP**: Ruta `ANY /core/{proxy+}` → ALB con HTTP_PROXY. CORS para el frontend en Amplify.
>
> 7. **CodePipeline**: Source desde GitHub `mkreder/grandt-backend` branch main (CodeStar connection), Build con CodeBuild (Docker privileged, push a ECR), Deploy a ECS.
>
> ### Orquestación
>
> ```
> VPC → ALB(VPC) → Aurora(VPC) → ECS(VPC, ECR, ALB, Aurora) → API Gateway(ALB) → Pipeline(ECR, ECS)
> ```
>
> ### Secrets necesarios
>
> ```bash
> pulumi config set --secret db_password "..."
> pulumi config set --secret secret_key "..."
> ```
