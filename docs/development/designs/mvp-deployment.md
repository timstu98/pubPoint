# MVP deployment

> **Accepted design**

## Goal and scope

Build the MVP locally, then deploy a private staging environment when its core journeys are ready for end-to-end validation. Use staging to find configuration and infrastructure problems before the first production release. It will use test data and separate credentials and configuration. The [MVP PRD](../../product/mvp-prd.md) does not prescribe a hosting platform.

## Decision

- Run the application containers on Amazon ECS with Fargate. ECS keeps the configured number of application tasks running; each task runs one or more containers. Fargate supplies the compute on hosts managed by AWS.
- Use Amazon RDS for MySQL for the database. Its expected cost better fits the current workload than Aurora MySQL-Compatible.
- Defer staging infrastructure during local MVP development. Deploy staging before production, with time to resolve issues found there. Plan the separate production environment when its capacity, availability, and release requirements are defined.

The project owner will also gain practical experience building and operating this AWS deployment.

## Alternatives considered

### Cloud provider

Google Cloud could host the application on [Cloud Run](https://cloud.google.com/run) with [Cloud SQL for MySQL](https://docs.cloud.google.com/sql/docs/mysql). Azure offers [Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/overview) with [Azure Database for MySQL](https://learn.microsoft.com/en-us/azure/mysql/flexible-server/overview). Both are credible managed options for a containerized application and MySQL database.

AWS is selected because ECS with Fargate and RDS fit the intended deployment model, and existing AWS familiarity reduces setup effort. Google Cloud and Azure remain viable if requirements or costs warrant a change.

### Deployment timing

| Option | Benefit | Trade-off |
| --- | --- | --- |
| Deploy staging early and keep it available | Finds cloud-specific problems while the MVP is small. | Pays for infrastructure that may see little use during several months of local development. |
| **Deploy for MVP validation (selected)** | Defers recurring cost while requirements settle, then checks the full application in AWS before production. | Finds cloud-specific problems later; allow time to fix them before release. |

### Application hosting

| Option | Benefit | Trade-off |
| --- | --- | --- |
| One server running Docker Compose, such as an EC2 instance or Lightsail VM | Simple, often inexpensive, and close to the local setup. | We maintain the server. A single host limits capacity and availability; expanding beyond it requires more infrastructure and operations work. |
| Hosted application platform, such as Railway or Render | Fast setup and fewer infrastructure tasks. | Less control over infrastructure. Private access and MySQL support depend on the provider and plan. |
| ECS on EC2 | ECS service management with direct control over the hosts; potentially lower compute cost at sustained scale. | We must provision, patch, and manage the EC2 capacity as well as the ECS service. |
| **ECS on Fargate (selected)** | Runs containers without host management, integrates with AWS services, and allows the service to run more tasks as demand grows. | More initial configuration than one server or a hosted platform; it may cost more for a small, continuously running service. |
| AWS Lambda | Scales with requests without continuously running application containers. | Requires adapting the current Flask container model and database connection approach. |

Using Fargate alone does not make staging highly available. Availability depends on task count, placement, traffic routing, and database configuration. Those choices also affect cost.

### Database

| Option | Benefit | Trade-off |
| --- | --- | --- |
| **RDS for MySQL (selected)** | Managed MySQL with a familiar engine and an expected lower cost for this small workload. | Does not include Aurora's specialized storage and availability features. |
| Aurora MySQL-Compatible | MySQL-compatible engine with additional storage, replication, and availability capabilities. | Its expected cost is higher for the MVP. Reconsider it if measured performance or fault-tolerance needs justify the expense. |
| Self-managed MySQL | More control and possibly a lower direct service charge. | We take responsibility for patching, backups, restores, and database availability. |

The application already uses MySQL, which both selected RDS and Aurora support. AWS supports migration from RDS for MySQL to Aurora MySQL, but a move would still need a tested plan. A PostgreSQL/PostGIS option for pub location search is also being evaluated; settle the database engine before provisioning RDS.

## Cost and implementation boundary

Rough monthly planning allowances in AWS London (USD, before VAT, credits, and paid external APIs):

| Stage | Assumption | Estimate |
| --- | --- | --- |
| Local MVP development | No ECS, RDS, or load balancer provisioned; CI and external services are outside this estimate. | **$0/month for staging infrastructure** |
| Staging validation | Small tasks run only when needed; small single-AZ RDS remains available during validation; no always-on load balancer or NAT gateway. | **$30-80/month while provisioned** |
| First live deployment | One or two small tasks run continuously, with small single-AZ RDS, load balancing, and basic networking and logs. | **$100-250/month** |
| Roughly 100,000-300,000 monthly active users | Millions of requests per month, more tasks, a larger or replicated database, and greater traffic and monitoring costs. | **$1,000-10,000+/month** |

These are broad allowances, not a priced architecture. Idle traffic does little to reduce the bill for resources that run all week; an always-on load balancer or NAT gateway would push staging toward the live-service range. Keeping staging alongside production adds its cost. Check the selected design in the [AWS Pricing Calculator](https://calculator.aws/) before provisioning.

During local development, CI should build deployable containers and run repository checks. The staging implementation plan will define the access method, networking, image registry, infrastructure code, deployment trigger, secrets, health checks, cost controls, and rollback procedure. Do not use real user data in staging. Production infrastructure and release policy remain outside this first deployment.

## References

- [AWS ECS on Fargate getting started](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/getting-started-fargate.html)
- [Amazon RDS for MySQL pricing](https://aws.amazon.com/rds/mysql/pricing/)
- [Amazon Aurora pricing](https://aws.amazon.com/rds/aurora/pricing/)
- [AWS Fargate pricing](https://aws.amazon.com/fargate/pricing/)
- [Elastic Load Balancing pricing](https://aws.amazon.com/elasticloadbalancing/pricing/)
- [Amazon VPC pricing](https://aws.amazon.com/vpc/pricing/)
- [Migrate an RDS for MySQL instance to Aurora MySQL](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Migrating.RDSMySQL.html)
