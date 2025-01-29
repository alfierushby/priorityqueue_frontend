from flask import Blueprint

from routes.priority import priority_router

routes = Blueprint('api',__name__, url_prefix='/api')

@routes.errorhandler(500)
def handle_generic_error(error):
    return {
        "error": "Internal Server Error",
        "message": "An unexpected error occurred",
        "error_type": "internal_error"
    }, 500

@routes.errorhandler(400)
def custom_error_400(msg):
    return {
        "error": "Error",
        "message": str(msg),
        "error_type": "internal_error"
    }, 400

@routes.errorhandler(KeyError)
def handle_key_error(error):
    return {
        "error": "Key Error",
        "message": "Required key(s) do not exist in request",
        "error_type": "internal_error"
    }, 400

@routes.errorhandler(ValueError)
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

@routes.errorhandler(TypeError)
def handle_type_error(error):
    return {
        "error": "Type Error",
        "message": "Required key(s) do not exist in request",
        "error_type": "internal_error"
    }, 400

routes.register_blueprint(priority_router)


