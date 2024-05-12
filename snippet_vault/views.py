import logging
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from utils.response import CustomResponse
from .models import Snippet, Tag
from .serializers import SnippetSerializer, TagSerializer

logger = logging.getLogger(__name__)


class SnippetViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Snippet model.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request) -> Response:
        """
        Retrieve a list of all snippets.

        Returns:
            Response: Response containing serialized data of all snippets.
        """

        snippets = self.filter_queryset(self.queryset)
        page = self.paginate_queryset(snippets)
        if page:
            serializer = self.get_serializer(
                page, many=True, context={"request": request}
            )
            data = self.get_paginated_response(serializer.data).data
            return CustomResponse.success(data=data)
        return CustomResponse.error(
            message="No data", status_code=status.HTTP_204_NO_CONTENT
        )

    def retrieve(self, request, *args, **kwargs) -> Response:
        """
        Retrieve a single snippet by its ID.


        Returns:
            Response: Response containing serialized data of the retrieved snippet or an error message.
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_data = serializer.data
        if "detail_page_url" in serializer_data:
            del serializer_data["detail_page_url"]
        return CustomResponse.success(data=serializer_data)

    def create(self, request, *args, **kwargs) -> Response:
        """
        Create a new snippet.


        Returns:
            Response: Response indicating success or failure of snippet creation.
        """

        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return CustomResponse.success(
            message="Snippet created successfully.",
            data=serializer.data,
            status_code=status.HTTP_201_CREATED,
        )

    def destroy(self, request, *args, **kwargs) -> Response:
        """
        Delete a snippet.

        Returns:
            Response: Response indicating success or failure of snippet deletion.
        """

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data
        if instance.user == self.request.user:
            instance.delete()
            return CustomResponse.success(data=data)
        return CustomResponse.error(
            message="Not Found", status_code=status.HTTP_404_NOT_FOUND
        )


class TagListAPIView(generics.ListAPIView):
    """
    API view to list all tags.
    """

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def list(self, request, *args, **kwargs) -> Response:
        """
        List all tags.


        Returns:
            Response: Response containing serialized data of all tags.
        """

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse.success(data=serializer.data)


class TagDetailAPIView(generics.ListAPIView):
    """
    API view to list snippets associated with a specific tag.
    """

    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs) -> Response:
        """
        List snippets associated with a specific tag.

        Args:
            request: HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, should contain 'tag_name'.

        Returns:
            Response: Response containing serialized data of snippets associated with the tag or an error message.
        """

        tag_name = kwargs["tag_name"]
        print('tag_name: ', tag_name)
        snippets = self.queryset.filter(tags__title__iexact=tag_name)
        page = self.paginate_queryset(snippets)
        if page:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data).data
            return CustomResponse.success(data=data)
        return CustomResponse.error(
            message="No data", status_code=status.HTTP_204_NO_CONTENT
        )
