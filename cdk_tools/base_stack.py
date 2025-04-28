import os
from aws_cdk import Stack
from constructs import Construct

DEFAULT_TEST_STACK_TTL = "3 days"


class BaseStack(Stack):
    """
    BaseStack for CDK applications enforcing consistent environment tagging.
    - Always sets the 'Environment' tag (either 'test' or 'live').
    - In 'test' environment, applies a TTL tag unless disabled.

    Args:
        scope (Construct): CDK scope.
        construct_id (str): Unique ID for the construct.
        ttl (str, optional): Time-to-live for test stacks, e.g., '3 days'.
                             Defaults to DEFAULT_TEST_STACK_TTL if None.
                             Pass an empty string '' to disable TTL tagging.
        **kwargs: Additional arguments passed to the Stack constructor.
    """

    def __init__(self, scope: Construct, construct_id: str, *, ttl: str = None, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.env_name = os.environ.get("ENV", "").lower()
        if self.env_name not in ["test", "live"]:
            raise ValueError("Please set ENV environment variable to 'test' or 'live'.")

        self.tags.set_tag("Environment", self.env_name)

        if self.env_name == "test":
            effective_ttl = ttl if ttl is not None else DEFAULT_TEST_STACK_TTL
            if effective_ttl:
                self.tags.set_tag("TTL", effective_ttl)
