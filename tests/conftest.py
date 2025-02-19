import boto3
import pytest
from dotenv import load_dotenv
from moto import mock_aws
from app import create_app
from containers import Container
from tests import test_routes

load_dotenv()

@pytest.fixture
def app():
    """Create and configure a new Flask app instance for testing
    :return: app created
    """
    with mock_aws():
        sqs = boto3.client("sqs", region_name="eu-north-1")

        #  Create mock queues
        low_queue = sqs.create_queue(QueueName="test-low")["QueueUrl"]
        medium_queue = sqs.create_queue(QueueName="test-medium")["QueueUrl"]
        high_queue = sqs.create_queue(QueueName="test-high")["QueueUrl"]

        # Set up container for testing
        container = Container()

        # Override SQS client with mock version
        container.sqs_client.override(sqs)

        # Override priority queues with test values
        container.priority_queues.override({
              "Low": low_queue,
              "Medium": medium_queue,
              "High": high_queue,
         })

        container.wire(modules=[test_routes])

        app = create_app(container)
        yield app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app
    :param app: The flask app
    :return: The app with a test client created
    """
    return app.test_client()
