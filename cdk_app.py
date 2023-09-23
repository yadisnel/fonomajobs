import os

import aws_cdk as cdk
from stacks.common_stack import CommonStack
from stacks.application_load_balancer import ApplicationLoadBalancerStack
from stacks.ecs_service import EcsServiceStack


STAGE = os.environ.get("STAGE", "dev")
env_eu = cdk.Environment(account="617563172979", region="eu-west-1")

app = cdk.App()


common_stack = CommonStack(
    app,
    f"api-common-stack-{STAGE}",
    env=env_eu,
)

ecs_service_stack = EcsServiceStack(
    app,
    f"fonoma-ecs-service-stack-{STAGE}",
    vpc=common_stack.vpc,
    env=env_eu,
)

application_load_balancer_stack = ApplicationLoadBalancerStack(
    app,
    f"fonoma-alb-stack-{STAGE}",
    vpc=common_stack.vpc,
    ecs_service=ecs_service_stack.ecs_service,
    env=env_eu,
)

app.synth()
