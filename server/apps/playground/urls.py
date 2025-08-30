from django.urls import path

from server.apps.playground.views import HiView,ItemListView,ItemDetailView, hello

urlpatterns = [
    # 指定使用者呼叫的位置： path("path",view位置)
    path("hello", hello),
    path(
        "hi", HiView.as_view()
    ),  # 預設承接的是一個方法，所以如果是class型態的就要用as_view()轉為方法
    path(
        "items", ItemListView.as_view()
    ), 
    path(
        "items/<int:item_id>", ItemDetailView.as_view()
    ),  #primerKey 通常會叫pk 也可以叫item_id 但切記不可以是id 因為python裡面有專屬id 如果用id 會導致python 的id 找不到
]
