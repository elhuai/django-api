from django.urls import path

from server.apps.playground.views import HiView, hello

urlpatterns = [
    # 指定使用者呼叫的位置： path("path",view位置)
    path("hello", hello),
    path(
        "hi", HiView.as_view()
    ),  # 預設承接的是一個方法，所以如果是class型態的就要用as_view()轉為方法
]
