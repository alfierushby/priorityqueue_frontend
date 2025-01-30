import os

import boto3
import pytest
from dotenv import load_dotenv
from moto import mock_aws
from app import create_app

load_dotenv()

@pytest.fixture
def app():
    """Create and configure a new Flask app instance for testing
    :return: app created
    """
    app = create_app()
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app
    :param app: The flask app
    :return: The app with a test client created
    """
    return app.test_client()


@pytest.fixture
def mock_env(app):
    """Mock AWS SQS and set environment variables for tests
    :param app: The flask app
    """
    with mock_aws():
        # Set up the mock SQS service
        sqs = boto3.client('sqs', region_name=app.config["AWS_REGION"])

        #  Create mock queues
        low_queue = sqs.create_queue(QueueName="test-low")["QueueUrl"]
        medium_queue = sqs.create_queue(QueueName="test-medium")["QueueUrl"]
        high_queue = sqs.create_queue(QueueName="test-high")["QueueUrl"]

        # Override app.config to use test queues
        app.config["PRIORITY_QUEUES"] = {
            "Low": low_queue,
            "Medium": medium_queue,
            "High": high_queue
        }

        yield
