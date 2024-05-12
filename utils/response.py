from typing import Optional, Union
from rest_framework.response import Response
from rest_framework import status


class CustomResponse:
    """
    Utility class for generating consistent API responses.
    """

    @staticmethod
    def success(
        message: str = "Success",
        data: Optional[Union[list, dict]] = None,
        status_code: int = status.HTTP_200_OK,
    ) -> Response:
        """
        Generate a success response.

        Args:
            message (str): A message describing the result.
            data (Optional[Union[list, dict]], optional): Additional data to include in the response. Defaults to None.
            status_code (int, optional): HTTP status code. Defaults to status.HTTP_200_OK.

        Returns:
            Response: The generated response.
        """
        response_data = {"success": True, "message": message}
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status_code)

    @staticmethod
    # def error(
    #     message: str = "error",
    #     errors: Optional[Union[str, dict, None]] = None,
    #     status_code: status = status.HTTP_400_BAD_REQUEST,
    # ) -> Response:
    def error(
        message = "error",
        errors = None,
        status_code = status.HTTP_400_BAD_REQUEST,
    ) -> Response:
        """
        Generate an error response.

        Args:
            message (str): A message describing the error.
            errors (Optional[Union[str, dict]], optional): Additional error details. Defaults to None.
            status_code (int, optional): HTTP status code. Defaults to status.HTTP_400_BAD_REQUEST.

        Returns:
            Response: The generated response.
        """
        response_data = {"success": False, "message": message}
        if errors is not None:
            response_data["errors"] = errors
        return Response(response_data, status=status_code)
