"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularJSONAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    # 指定使用者呼叫的位置： path("path",view位置)
    path("admin/", admin.site.urls),
    # path(
    #     "api/v1/playground/", include("server.apps.playground.urls")
    # ),  # 前綴方式可以連接到各種不同的apps 讓apps個字的功能就可以連動到各自的urls
    path("api/v1/todo/", include("server.apps.todo.urls")),
    # API
    path(
        "api/docs/schema.json", SpectacularJSONAPIView.as_view(), name="schema"
    ),  # 生成json檔案
    path(
        "api/docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger",
    ),  # 生成可以測試的api文件
    path(
        "api/docs/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),  # 生成僅供閱讀的api文件
    # TOKEN
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),  # 產生login 跟logout API
    path("api/auth/", include("djoser.urls.jwt")),  # jwt
]
