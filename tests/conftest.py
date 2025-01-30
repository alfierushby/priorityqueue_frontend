import os

import boto3
import pytest
from dotenv import load_dotenv
from moto import mock_aws
from app import create_app

load_dotenv()

AWS_REGION = os.getenv('AWS_REGION')


@pytest.fixture
def app():
    """Create and configure a new Flask app instance for testing"""
    app = create_app(testing=True)
    return app


@pytest.fixture
def client(app):
    """Create a test client for the Flask app"""
    return app.test_client()


@pytest.fixture
def mock_env(app):
    """Mock AWS SQS and set environment variables for tests"""
    with mock_aws():
        # Set up the mock SQS service
        sqs = boto3.client('sqs', region_name=AWS_REGION)

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
