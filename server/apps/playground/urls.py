from django.urls import include, path
from rest_framework.routers import DefaultRouter

from server.apps.playground.views import (
    HiView,
    # ItemListView,
    # ItemDetailView,
    ItemViewSet,
    hello,
)

# ViewSet的話請要用router註冊
router = DefaultRouter(trailing_slash=False)  # 產生的 router 不要有結尾的"/"
router.register(
    "items-v2", ItemViewSet
)  # 要從views裡面引入ItemViewSet ->用 router.register 去產生 "items-v2" 跟 "items/<int:item_id>" 這兩個路徑到router.urls
urlpatterns = [
    # 指定使用者呼叫的位置： path("path",view位置)
    path("hello", hello),
    path(
        "hi", HiView.as_view()
    ),  # 預設承接的是一個方法，所以如果是class型態的就要用as_view()轉為方法
    # path("items", ItemListView.as_view()),
    # path("items/<int:item_id>", ItemDetailView.as_view()),
    # primerKey 通常會叫pk 也可以叫item_id 但切記不可以是id ，如果不叫pk的話 就是後續處理串入值時要 特別設定 lookup_url_kwarg = "item_id"
    # 因為python裡面有專屬id 如果用id 會導致python 的id 找不到
    path(
        "viewset/", include(router.urls)
    ),  # 當使用者請求使用的是viewset時 就去router.urls找套件繼承的方法
]
