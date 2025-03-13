import os

from dependency_injector import containers, providers
import boto3


class Container(containers.DeclarativeContainer):
    """Dependency injection container for Flask"""

    config = providers.Configuration()

    # Singleton so that the application only has one sqs on runtime. Can be overridden for testing
    sqs_client = providers.Singleton(
        boto3.client,
        service_name="sqs",
        region_name=config.aws_region,
    )

    bedrock_client = providers.Singleton(
        boto3.client,
        service_name="bedrock-runtime",
        region_name="us-east-1",
    )

    # Queue URLs provider
    priority_queues = providers.Object({
        "Low": os.getenv("P1_QUEUE_URL", "test-low"),
        "Medium": os.getenv("P2_QUEUE_URL", "test-medium"),
        "High": os.getenv("P3_QUEUE_URL", "test-high"),
    })

