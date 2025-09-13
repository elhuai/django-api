from django.contrib.auth import get_user_model
from rest_framework.serializers import (
    CurrentUserDefault,
    HiddenField,
    ModelSerializer,
)

from server.apps.todo.models import Project, Tag, Task

User = get_user_model()


class OwnerSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ProjectSerializer(ModelSerializer):
    # owner = HiddenField(default=CurrentUserDefault())
    # 使用者無法指定 owner 。 系統會自動把 request.user 填進去
    # 如果參與了unique
    owner_id = HiddenField(
        default=CurrentUserDefault(),
        source="owner",
        write_only=True,
    )
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "owner",
            "owner_id",
            "is_public",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "owner"
        ]  # 讓前端可以看到 owner 是誰。 防止使用者在 POST 或 PUT 中手動指定 owner（防止偽造或越權）


class TagSerializer(ModelSerializer):
    owner_id = HiddenField(
        default=CurrentUserDefault(), source="owner", write_only=True
    )

    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "owner", "owner_id", "created_at", "updated_at"]
        read_only_fields = ["owner"]


class TaskSerializer(ModelSerializer):
    # owner = HiddenField(default=CurrentUserDefault())
    owner_id = HiddenField(
        default=CurrentUserDefault(),
        source="owner",
        write_only=True,
    )
    owner = OwnerSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "priority",
            "is_completed",
            "due_date",
            "owner",
            "owner_id",
            "project",
            "tags",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["owner"]
