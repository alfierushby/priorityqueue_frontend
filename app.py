import os

from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
from prometheus_flask_exporter import PrometheusMetrics

from containers import Container
from routes import blueprint_routes, priority

load_dotenv()

def create_app(container: Container = None):
    """Application factory function for testing"""
    app = Flask(__name__)

    # Initialize DI container if not provided
    if container is None:
        container = Container()
        container.config.from_dict({
            "aws_region": os.getenv("AWS_REGION"),
            "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
            "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        })

    # Wire dependencies into routes
    container.wire(modules=[priority])

    metrics = PrometheusMetrics(app)

    # Register blueprints
    app.register_blueprint(blueprint_routes)

    @app.route('/', methods=["GET"])
    def index():
        return render_template("index.html")

    @app.route('/health', methods=["GET"])
    def health_check():
        """ Checks health, endpoint """
        return jsonify({"status": "healthy"}), 200

    return app


if __name__ == '__main__':
    create_app().run()
