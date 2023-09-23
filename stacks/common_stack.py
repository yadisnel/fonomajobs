import os

from aws_cdk import Duration, RemovalPolicy, Stack, aws_ec2, aws_ecr, aws_iam, aws_ssm
from constructs import Construct

STAGE = os.environ.get("STAGE", "dev")


class CommonStack(Stack):
    vpc: aws_ec2.Vpc
    ecr_repository: aws_ecr.Repository

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.is_production = STAGE == "prod"
        self.vpc = None
        self.ecs_cluster = None

        # Setup vpc
        self.setup_vpc()
        # ECR repository
        self.setup_ecr_repository()

    def setup_vpc(self):
        self.vpc = aws_ec2.Vpc(
            self,
            f"vpc-{STAGE}",
            vpc_name=f"vpc-{STAGE}",
            ip_addresses=aws_ec2.IpAddresses.cidr("10.0.0.0/16"),
            nat_gateways=0,
            max_azs=3,
            subnet_configuration=[
                aws_ec2.SubnetConfiguration(
                    name=f"private-subnet-1-{STAGE}",
                    cidr_mask=24,
                    subnet_type=aws_ec2.SubnetType.PRIVATE_WITH_EGRESS,
                ),
                aws_ec2.SubnetConfiguration(
                    name=f"public-subnet-1-{STAGE}",
                    cidr_mask=24,
                    subnet_type=aws_ec2.SubnetType.PUBLIC,
                ),
                aws_ec2.SubnetConfiguration(
                    name=f"isolate-subnet-1-{STAGE}",
                    cidr_mask=28,
                    subnet_type=aws_ec2.SubnetType.PRIVATE_ISOLATED,
                ),
            ],
        )

        aws_ssm.StringParameter(
            self,
            f"vpc-id-parameter-{STAGE}",
            description="VPC ID",
            parameter_name=f"/infra/vpc-id/{STAGE}",
            string_value=self.vpc.vpc_id,
            tier=aws_ssm.ParameterTier.STANDARD,
        )

    def setup_ecr_repository(self):
        deploy_role = aws_iam.Role.from_role_name(
            self, f"ecr-deploy-role-{STAGE}", role_name="github-actions-role"
        )

        self.ecr_repository = aws_ecr.Repository(
            self,
            f"ecr-repository-{STAGE}",
            image_scan_on_push=False,
            image_tag_mutability=aws_ecr.TagMutability.MUTABLE,
            repository_name=f"ecr-repository-{STAGE}",
            lifecycle_rules=[
                aws_ecr.LifecycleRule(
                    max_image_age=Duration.days(30),
                    tag_status=aws_ecr.TagStatus.UNTAGGED,
                )
            ],
            removal_policy=RemovalPolicy.RETAIN
            if self.is_production
            else RemovalPolicy.DESTROY,
        )
        self.ecr_repository.grant_pull_push(deploy_role)
