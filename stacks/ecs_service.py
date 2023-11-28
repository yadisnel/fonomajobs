import os

from aws_cdk import (
    RemovalPolicy,
    Stack,
    aws_ec2,
    aws_ecs,
    aws_logs,
    aws_route53,
)
from constructs import Construct

from stacks.utils import UtilsService


class EcsServiceStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        vpc: aws_ec2.Vpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = vpc
        self.stage = os.environ.get("STAGE", "dev")
        self.is_production = self.stage == "prod"
        self.ecs_service = None
        self.hosted_zone = None

        # Setup common resources
        self.setup_common_resources()
        # Setup ecs service
        self.setup_ecs_service()

    def setup_common_resources(self):
        self.hosted_zone = aws_route53.HostedZone.from_lookup(
            self,
            f"hosted-zone-{self.stage}",
            domain_name="fonomajobs.com",
        )

    def setup_ecs_service(self):
        cluster = aws_ecs.Cluster(
            self,
            f"fonoma-ecs-cluster-{self.stage}",
            vpc=self.vpc,
            cluster_name=f"ecs-cluster-{self.stage}",
            container_insights=True,
        )

        # Create Task Definition
        task_definition = aws_ecs.FargateTaskDefinition(
            self, f"aws_iam-api-ecs-task-{self.stage}",
            cpu=256,
            memory_limit_mib=512,
        )

        task_definition_log_group = aws_logs.LogGroup(
            self,
            f"fonoma-api-task-group-{self.stage}",
            log_group_name=f"fonoma-api-task-group-{self.stage}",
            removal_policy=RemovalPolicy.RETAIN,
            retention=aws_logs.RetentionDays.THREE_MONTHS,
        )

        container = task_definition.add_container(
            f"fonoma-api-container-{self.stage}",
            image=aws_ecs.ContainerImage.from_asset(
                directory=UtilsService.root_dir(),
                file="Dockerfile",
            ),
            cpu=256,
            memory_limit_mib=512,
            logging=aws_ecs.LogDriver.aws_logs(
                stream_prefix=f"fonoma-api-{self.stage}",
                log_group=task_definition_log_group,
            ),
            environment={
                "STAGE": self.stage,
                "COMMIT_HASH": "latest",
            }
        )

        port_mapping = aws_ecs.PortMapping(
            container_port=80, protocol=aws_ecs.Protocol.TCP
        )

        container.add_port_mappings(port_mapping)

        # Create Service
        self.ecs_service = aws_ecs.FargateService(
            self,
            f"fonoma-api-service-{self.stage}",
            service_name=f"fonoma-api-service-{self.stage}",
            cluster=cluster,
            task_definition=task_definition,
            vpc_subnets=aws_ec2.SubnetSelection(
                subnet_type=aws_ec2.SubnetType.PUBLIC,
            ),
            assign_public_ip=True,
            desired_count=1,
            circuit_breaker=aws_ecs.DeploymentCircuitBreaker(rollback=True),
            min_healthy_percent=100,
            max_healthy_percent=200,
        )

        task_scaling = self.ecs_service.auto_scale_task_count(
            min_capacity=1,
            max_capacity=2,
        )

        task_scaling.scale_on_cpu_utilization(
            f"fonoma-api-service-cpu-scaling-{self.stage}",
            target_utilization_percent=85,
        )
