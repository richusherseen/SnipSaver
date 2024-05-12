from typing import Any, Dict, List
from rest_framework.reverse import reverse
from rest_framework import serializers
from .models import Snippet, Tag
from rest_framework.exceptions import PermissionDenied


class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for Tag model.
    """

    class Meta:
        model = Tag
        fields = ("id", "title")


class SnippetSerializer(serializers.ModelSerializer):
    """
    Serializer for Snippet model.
    """

    tags = TagSerializer(many=True)
    created_by = serializers.SerializerMethodField()
    detail_page_url = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = (
            "id",
            "title",
            "content",
            "tags",
            "created_by",
            "created_at",
            "detail_page_url",
        )
        read_only_fields = ("id", "created_by", "created_at", "detail_page_url")

    def validate_title(self, value: str) -> str:
        """
        Validate the title field.
        """
        if not value:
            raise serializers.ValidationError("Title field is required.")
        return value

    def validate_content(self, value: str) -> str:
        """
        Validate the content field.
        """
        if not value:
            raise serializers.ValidationError("Content field is required.")
        return value

    def validate_tags(self, value: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Validate the tags field.
        """
        if not value:
            raise serializers.ValidationError("Tags field is required.")

        tag_titles = [tag_data["title"] for tag_data in value]
        if len(tag_titles) != len(set(tag_titles)):
            raise serializers.ValidationError("Duplicate tags are not allowed.")

        return value

    def get_detail_page_url(self, obj: Snippet) -> str:
        """
        Method to get the URL of the snippet detail API.
        """
        request = self.context.get("request")
        return reverse("snippet-detail", args=[obj.id], request=request)

    def get_created_by(self, obj: Snippet) -> str:
        """
        Method to get the username of the user who created the snippet.
        """
        return obj.user.username

    def create(self, validated_data: Dict[str, Any]) -> Snippet:
        """
        Create a new snippet instance.

        Args:
            validated_data (dict): The validated data for the snippet.

        Returns:
            Snippet: The newly created snippet instance.
        """
        tags_data = validated_data.pop("tags")

        tags = []
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(title=tag_data["title"])
            tags.append(tag)
        snippet = Snippet.objects.create(
            user=self.context["request"].user, **validated_data
        )
        snippet.tags.add(*tags)

        return snippet

    def update(self, instance: Snippet, validated_data: Dict[str, Any]) -> Snippet:
        """
        Update an existing snippet instance.

        Args:
            instance (Snippet): The snippet instance to be updated.
            validated_data (dict): The validated data for the update.

        Returns:
            Snippet: The updated snippet instance.
        """
        if self.context["request"].user != instance.user:
            raise PermissionDenied("You do not have permission to perform this action.")
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)

        if "tags" in validated_data:
            new_tags_data = validated_data.pop("tags")
            new_tags = []
            for tag_data in new_tags_data:
                tag, _ = Tag.objects.get_or_create(title=tag_data["title"])
                new_tags.append(tag)
            instance.tags.set(new_tags)

        instance.save()
        return instance
