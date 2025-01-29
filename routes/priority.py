import os

import boto3
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify, render_template, abort

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


@priority_router.post('/')
def priority_post():
    title = request.form.get("title","Default")
    description = request.form.get("description","Default Description")
    priority = request.form.get("priority","Unknown")

    if priority == "" or description == "" or title == "":
        abort(400, description="One or more of your fields are empty")

    queue_url = PRIORITY_QUEUES[priority]

    message_body = {
        "title": title,
        "description": description,
        "priority": priority
    }

    sqs_client.send_message(QueueUrl=queue_url, MessageBody=str(message_body))

    return render_template("index.html")
