import os

from aws_cdk import (
    Duration,
    Stack,
    aws_autoscaling,
    aws_certificatemanager,
    aws_ec2,
    aws_ecs,
    aws_elasticloadbalancingv2,
    aws_route53,
    aws_route53_targets,
)
from constructs import Construct


class ApplicationLoadBalancerStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        ecs_service: aws_ecs.Ec2Service,
        vpc: aws_ec2.Vpc,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = vpc
        self.stage = os.environ.get("STAGE", "dev")
        self.is_production = self.stage == "prod"
        self.ecs_service = ecs_service
        self.hosted_zone = None
        self.application_load_balancer = None

        # Setup common resources
        self.setup_common_resources()
        # Setup application load balancer
        self.setup_application_load_balancer()

    def setup_common_resources(self):
        self.hosted_zone = aws_route53.HostedZone.from_lookup(
            self,
            f"hosted-zone-{self.stage}",
            domain_name="fonomajobs.com",
        )

    def setup_application_load_balancer(self):
        self.application_load_balancer = (
            aws_elasticloadbalancingv2.ApplicationLoadBalancer(
                self,
                f"application-load-balancer-{self.stage}",
                load_balancer_name=f"application-load-balancer-{self.stage}",
                vpc=self.vpc,
                internet_facing=True,
            )
        )
        certificate = aws_certificatemanager.Certificate(
            self,
            f"certificate-{self.stage}",
            domain_name="fonomajobs.com",
            subject_alternative_names=[
                "*.fonomajobs.com",
            ],
            validation=aws_certificatemanager.CertificateValidation.from_dns(
                self.hosted_zone
            ),
        )

        listener_443 = self.application_load_balancer.add_listener(
            f"listener-443-{self.stage}",
            port=443,
            open=True,
            certificates=[
                certificate,
            ],
        )

        health_check = aws_elasticloadbalancingv2.HealthCheck(
            interval=Duration.seconds(60),
            path="/health",
            timeout=Duration.seconds(5),
        )

        listener_443.add_targets(
            f"target-ecs-service-{self.stage}",
            port=80,
            targets=[self.ecs_service],
            health_check=health_check,
        )

        self.application_load_balancer.add_listener(
            f"listener-80-{self.stage}",
            port=80,
            open=True,
            default_action=aws_elasticloadbalancingv2.ListenerAction.redirect(
                port="443",
                protocol="HTTPS",
                permanent=True,
            ),
        )

        aws_route53.ARecord(
            self,
            f"alias-record-{self.stage}",
            zone=self.hosted_zone,
            record_name="fonomajobs.com",
            target=aws_route53.RecordTarget.from_alias(
                aws_route53_targets.LoadBalancerTarget(self.application_load_balancer)
            ),
        )
