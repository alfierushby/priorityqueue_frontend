from botocore.exceptions import ClientError
from flask import Blueprint
from pydantic import ValidationError

from routes.priority import priority_router

blueprint_routes = Blueprint('api',__name__, url_prefix='/api')

@blueprint_routes.errorhandler(500)
def handle_generic_error(error):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "error_type": "internal_error"
    }, 500

@blueprint_routes.errorhandler(ValidationError)
def handle_validation_error(error):
    # Extract only user-friendly messages without exposing internal structure
    simplified_errors = [
        {"field": err.get("loc", ["Unknown"]),
         "message": err.get("msg", "Invalid value")}
        for err in error.errors()
    ]

    return {
        "error": "Validation Error",
        "message": "There were issues with the data provided.",
        "error_type": "validation_error",
        "details": simplified_errors  # Contains only high-level validation issues
    }, 400

@blueprint_routes.errorhandler(400)
def custom_error_400(msg):
    return {
        "error": "Error",
        "message": str(msg),
        "error_type": "internal_error"
    }, 400

@blueprint_routes.errorhandler(KeyError)
def handle_key_error(error):
    return {
        "error": "Key Error",
        "message": "Required key(s) do not exist in request",
        "error_type": "internal_error"
    }, 400

@blueprint_routes.errorhandler(ClientError)
def handle_client_error(error):
    return {
        "error": "Client boto3 Error",
        "message": error.response,
        "error_type": "internal_error"
    }, 400

@blueprint_routes.errorhandler(ValueError)
def handle_value_error(error):
    if "list.remove(x)" in error.args[0]:
        return {
            "error": "Removal Error",
            "message": "Cannot remove the entity because it doesn't exist in the list",
            "error_type": "removal_error"
        }, 400
    else:
        return {
            "error": "Invalid Value",
            "message": "One or more field values are invalid",
            "error_type": "value_error"
        }, 400

@blueprint_routes.errorhandler(TypeError)
def handle_type_error(error):
    return {
        "error": "Type Error",
        "message": "Required key(s) do not exist in request",
        "error_type": "internal_error"
    }, 400

blueprint_routes.register_blueprint(priority_router)


