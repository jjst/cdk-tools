import os
from aws_cdk import Stack
from constructs import Construct


class BaseStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        self.env_name = os.environ.get("ENV", "").lower()
        if self.env_name not in ["test", "live"]:
            raise ValueError("Please set ENV to 'test' or 'live'.")

        self.tags.set_tag("Environment", self.env_name)

        if self.env_name == "test":
            self.tags.set_tag("TTL", "3 days")
