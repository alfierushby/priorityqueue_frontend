import boto3
import pytest
from moto import mock_aws
from app import create_app


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
def mock_env(monkeypatch):
    """Mock AWS SQS and set environment variables for tests"""
    with mock_aws():
        # Set up the mock SQS service
        sqs = boto3.client('sqs', region_name='eu-north-1')
        queue_url = sqs.create_queue(QueueName='test-queue')['QueueUrl']

        # Mock the environment variable
        monkeypatch.setenv('P1_QUEUE_URL', queue_url)

        yield
