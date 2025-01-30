import os

from moto import mock_aws
import boto3

@mock_aws
def test_priority_post(client):
    # Set up the mock SQS service
    response = client.post("/api/priority/", data={
        "title": "Urgent Issue",
        "description": "Fix ASAP",
        "priority": "Medium"
    })

    assert response.status_code == 302

    queue_url = os.environ["P1_QUEUE_URL"]
    sqs = boto3.client("sqs", region_name="eu-north-1")
    messages = sqs.receive_message(QueueUrl=queue_url)

    assert "Messages" in messages
    assert len(messages["Messages"]) == 1