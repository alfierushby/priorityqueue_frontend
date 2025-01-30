import boto3
from moto import mock_aws


def general_priority_post(client, mock_env, priority):
    """Test posting a priority request with form data"""

    # Get the correct queue URL from Flask's test config
    queue_url = client.application.config["PRIORITY_QUEUES"][priority]

    # Ensure we use the same region as in mock_env
    sqs = boto3.client("sqs", region_name=client.application.config["AWS_REGION"])

    # Simulate form submission
    response = client.post("/api/priority/", data={
        "title": "Urgent Issue",
        "description": "Fix ASAP",
        "priority": priority
    }, content_type="application/x-www-form-urlencoded")

    assert response.status_code == 302

    # Check if the message was sent to the correct mock SQS queue
    messages = sqs.receive_message(QueueUrl=queue_url)
    assert "Messages" in messages
    assert len(messages["Messages"]) == 1
    assert "Urgent Issue" in messages["Messages"][0]["Body"]
    assert "Fix ASAP" in messages["Messages"][0]["Body"]
    assert priority in messages["Messages"][0]["Body"]


def test_medium_priority_post(client, mock_env):
    """Test posting a medium priority request with form data"""
    general_priority_post(client, mock_env, "Medium")


def test_low_priority_post(client, mock_env):
    """Test posting a low priority request with form data"""
    general_priority_post(client, mock_env, "Low")


def test_high_priority_post(client, mock_env):
    """Test posting a high priority request with form data"""
    general_priority_post(client, mock_env, "High")


def test_empty_string_description_post(client, mock_env):
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


def test_null_description_post(client, mock_env):
    """Test a wrong post"""
    # Simulate form submission
    response = client.post("/api/priority/", data={
        "title": "Urgent Issue",
        "priority": "Medium"
    }, content_type="application/x-www-form-urlencoded")

    assert response.status_code == 400

    error_data = response.get_json()

    assert error_data["error_type"] == "validation_error"
    expected_error = {
        "field": ["description"],
        "message": "Input should be a valid string"
    }
    assert expected_error in error_data["details"]


def test_null_post(client, mock_env):
    """Test a wrong post"""
    # Simulate form submission
    response = client.post("/api/priority/", data={
    }, content_type="application/x-www-form-urlencoded")

    assert response.status_code == 400

    error_data = response.get_json()

    assert error_data["error_type"] == "validation_error"
    expected_errors = [{
        "field": ["description"],
        "message": "Input should be a valid string"
    },
        {
            "field": ["title"],
            "message": "Input should be a valid string"
        },
        {
            "field": ["priority"],
            "message": "Input should be a valid string"
        }
    ]
    for expected_error in expected_errors: assert expected_error in error_data["details"]
