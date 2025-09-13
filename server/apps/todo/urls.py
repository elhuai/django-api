from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server.apps.todo.views import (
    ProjectViewSet,
    TagViewSet,
    TaskViewSet,
)

# ViewSet的話請要用router註冊
router = DefaultRouter(trailing_slash=False)  # 產生的 router 不要有結尾的"/"
router.register("projects", ProjectViewSet)
router.register("tags", TagViewSet)
router.register("tasks", TaskViewSet)

urlpatterns = [
    path(
        "", include(router.urls)
    ),  # 當使用者請求使用的是viewset時 就去router.urls找套件繼承的方法
]
