from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is not None:
        if hasattr(context["view"], "error_message"):
            error_message = context["view"].error_message
        else:
            error_message = "Error de validación"

        if "detail" in response.data:
            new_response = {
                "error": response.data["detail"],
            }
        else:
            new_response = {
                "error": error_message,
                "detail": response.data,
            }
        return Response(data=new_response, status=response.status_code)
    return response
