import boto3

def test_priority_post(client, mock_env):
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
    assert "Fix ASAP" in messages["Messages"][0]["Body"]
    assert "Medium" in messages["Messages"][0]["Body"]


def test_wrong_post(client, mock_env):
    """Test a wrong post"""
    # Simulate form submission
    response = client.post("/api/priority/", data={
        "title": "Urgent Issue",
        "description": "",
        "priority": "Medium"
    }, content_type="application/x-www-form-urlencoded")

    assert response.status_code == 400

    error_data = response.get_json()

    assert error_data["error_type"] == "validation_error"
    expected_error = {
        "field": ["description"],
        "message": "String should have at least 1 character"
    }
    assert expected_error in error_data["details"]