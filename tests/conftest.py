import io
import json
import os
from unittest.mock import MagicMock, Mock

import boto3
import pytest
from dotenv import load_dotenv
from moto import mock_aws
from app import create_app
from containers import Container
from tests import test_routes

load_dotenv()

mock_body = Mock()
mock_body.read.return_value = json.dumps({"results" : [{"outputText" : "Testing"}]})

mock_response = {"body": mock_body}


@pytest.fixture
def app():
    """Create and configure a new Flask app instance for testing
    :return: app created
    """
    with mock_aws():
            sqs = boto3.client("sqs", region_name=os.getenv("AWS_REGION"))
            bedrock = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))

            bedrock.invoke_model = MagicMock(return_value=mock_response)

            #  Create mock queues
            low_queue = sqs.create_queue(QueueName="test-low")["QueueUrl"]
            medium_queue = sqs.create_queue(QueueName="test-medium")["QueueUrl"]
            high_queue = sqs.create_queue(QueueName="test-high")["QueueUrl"]

            # Set up container for testing
            container = Container()

            # Override SQS client with mock version
            container.sqs_client.override(sqs)

            # Override bedrock client with mock version
            container.bedrock_client.override(bedrock)

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
