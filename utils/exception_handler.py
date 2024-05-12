import logging
from typing import Any, Dict
from rest_framework.views import exception_handler
from rest_framework import status
from .response import CustomResponse
from rest_framework.exceptions import APIException


logger = logging.getLogger(__name__)


def custom_exception_handler(
    exc: APIException, context: Dict[str, Any]
) -> CustomResponse:
    """
    Custom exception handler to format API responses.

    Args:
        exc (APIException): The exception raised during request processing.
        context (dict): Context containing request and view information.

    Returns:
        Union[CustomResponse, None]: Customized response.
    """

    logger.error("An error occurred while processing the request:", exc_info=exc)

    response = exception_handler(exc, context)

    if response is None:
        return CustomResponse.error(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="An error occurred while processing the request. Please try again later.",
        )

    elif response.status_code == 404:
        return CustomResponse.error(
            status_code=status.HTTP_404_NOT_FOUND,
            message="Not found!",
        )
    else:
        return CustomResponse.error(
            status_code=response.status_code,
            message=exc.default_detail,
            errors=exc.detail,
        )
