import os
import time

import boto3
from dotenv import load_dotenv
from flask import Blueprint, request, render_template, abort, url_for, redirect, current_app
from prometheus_flask_exporter import Counter, Histogram
from pydantic import BaseModel, Field

load_dotenv()

# Create a "Blueprint" or module
priority_router = Blueprint('priority', __name__, url_prefix='/priority')
AWS_REGION = os.getenv('AWS_REGION')
ACCESS_KEY = os.getenv('AWS_ACCESS_KEY_ID')
ACCESS_SECRET = os.getenv('AWS_SECRET_ACCESS_KEY')

sqs_client = boto3.client('sqs', region_name=AWS_REGION, aws_access_key_id=ACCESS_KEY
                          , aws_secret_access_key=ACCESS_SECRET)

# Use the existing PrometheusMetrics instance in `app.py`
request_counter = Counter(
    "priority_requests_total",
    "Total priority requests processed",
    labelnames=["priority"]
)

request_latency = Histogram(
    "priority_request_latency_seconds",
    "Latency of priority requests",
    labelnames=["priority"],
    buckets=(0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0)
)


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
    start_time = time.time()

    title = request.form.get("title", "Default")
    description = request.form.get("description", "Default Description")
    priority = request.form.get("priority", "Unknown")

    external_data = {
        "title": title,
        "description": description,
        "priority": priority
    }

    message = Request(**external_data)

    priority_queues = current_app.config["PRIORITY_QUEUES"]
    queue_url = priority_queues[priority]

    sqs_client.send_message(QueueUrl=queue_url, MessageBody=message.model_dump_json())

    # Track metrics
    request_counter.labels(priority=priority).inc()
    request_latency.labels(priority=priority).observe(time.time() - start_time)

    return redirect(url_for("index"))
