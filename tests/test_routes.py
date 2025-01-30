import os

from moto import mock_aws
import boto3

@mock_aws
def test_medium_priority_post(client, mock_env):
    """Test posting a priority request with form data"""

    # Get the correct queue URL from Flask's test config
    queue_url = client.application.config["PRIORITY_QUEUES"]["Medium"]

    # Ensure we use the same region as in mock_env
    sqs = boto3.client("sqs", region_name=client.application.config["AWS_REGION"])

    # Simulate form submission
    response = client.post("/api/priority/", data={
        "title": "Urgent Issue",
        "description": "Fix ASAP",
        "priority": "Medium"
    }, content_type="application/x-www-form-urlencoded")

    assert response.status_code == 302

    # Check if the message was sent to the correct mock SQS queue
    messages = sqs.receive_message(QueueUrl=queue_url)
    assert "Messages" in messages
    assert len(messages["Messages"]) == 1
    assert "Urgent Issue" in messages["Messages"][0]["Body"]

