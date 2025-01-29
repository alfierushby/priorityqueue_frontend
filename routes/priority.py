import os

import boto3
from dotenv import load_dotenv
from flask import Blueprint, request, render_template, abort, url_for, redirect
from pydantic import BaseModel, Field

load_dotenv()

# Create a "Blueprint" or module
priority_router = Blueprint('priority', __name__, url_prefix='/priority')
AWS_REGION = os.getenv('AWS_REGION')
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
ACCESS_SECRET = os.getenv('AWS_SECRET_ACCESS_KEY')

sqs_client = boto3.client('sqs', region_name=AWS_REGION, aws_access_key_id=ACCESS_KEY
                          , aws_secret_access_key=ACCESS_SECRET)

PRIORITY_QUEUES = {
    "Low": os.getenv("P1_QUEUE_URL"),
    "Medium": os.getenv("P2_QUEUE_URL"),
    "High": os.getenv("P3_QUEUE_URL")
}

# Want the minimum length to be at least 1, otherwise "" can be sent which breaks certain APIs.
class Request(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    priority: str = Field(..., min_length=1)


@priority_router.post('/')
def priority_post():
    """
    Adds a priority to a specified SQS queue, with validation
    :return: The html site to do it again
    """
    title = request.form.get("title", "Default")
    description = request.form.get("description", "Default Description")
    priority = request.form.get("priority", "Unknown")

    external_data = {
        "title": title,
        "description": description,
        "priority": priority
    }

    message = Request(**external_data)

    queue_url = PRIORITY_QUEUES[priority]

    sqs_client.send_message(QueueUrl=queue_url, MessageBody=message.model_dump_json())

    return redirect(url_for("index"))
