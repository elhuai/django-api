from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from server.apps.playground.models import Item
from server.apps.playground.serializers import ItemSerializer

from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

# from rest_framework.mixins import (
#     CreateModelMixin,  # 負責處理建立 (POST)
#     DestroyModelMixin,  # 負責處理刪除 (DELETE)
#     ListModelMixin,  # 負責列表 (GET)
#     RetrieveModelMixin,  # 負責單一物件存取 (GET)
#     UpdateModelMixin,  # 負責更新 (PUT, PATCH)
# )


@api_view(["GET", "POST"])  # 限定打api的方法
def hello(request):  # django 裡面的view都要接request這個參數
    if request.method == "GET":
        message = "GET success"
    elif request.method == "POST":
        message = "POST success"

    return Response({"message": message})


# api寫成class的好處是可以制定自己的method
class HiView(APIView):
    # 有self 是因爲出現在class當中 #但因為是api所以要有request參數

    def _build_message(self, method):
        return f"Hi with {method} Method"

    def get(self, request):
        return Response({"message": self._build_message("GET")})

    def post(self, request):
        return Response({"message": self._build_message("POST")})


# GET /xxxxxx/items => 得到資料庫中所有的 Items
# 第一寫法：使用框架 (把取資料方式改為通用方式，不要很多地方都用相同的語法)
# class ItemListView(ListCreateAPIView):
#     serializer_class = ItemSerializer
#     queryset = Item.objects.all()


# 第二種寫法：()

#
# from rest_framework.generics import GenericAPIView

# from rest_framework.mixins import CreateModelMixin, ListModelMixin
# class ItemListView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     def get(self, request):
#         return self.list(request)

#     def post(self, request):
#         return self.create(request)


# 第二寫法： 原始的寫法
"""
class ItemListView(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)  # 括號中裡面處理商業邏輯
        return Response(serializer.data)

    # 新增資料 要經過序列化清洗，把多的欄位移除，以確保拿到的資料是正確的
    def post(self, request):
        serializer = ItemSerializer(data=request.data)

        # 方法一：用ＯＲＭ去做
        # # ItemSerializer 序列化清洗 去驗證 request.data 是否合法可以被使用
        # if not serializer.is_valid():  # 沒有通過認證的話400 (使用者傳進資料有錯)
        #     return Response(serializer.errors, status=400)
        # # **語法糖將資料解成變數型態
        # Item.objects.create(**serializer.validated_data)

        # 方法二：用框架裡面的預設做（推薦）
        # 利用 is_valid() 自動驗證資料，遇到錯誤就直接丟出例外並回應錯誤訊息
        serializer.is_valid(raise_exception=True)
        serializer.save()  # 完成新增

        return Response({"status": "OK "}, status=201)
"""


# GET /xxxxxx/items/<id> => 得到資料庫中指定的 Items

"""版本一寫法
class ItemDetailView(
    RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericAPIView
):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()  # 設定可以修改的範圍
    # 如果說有需要篩選的話可以寫成  Item.objects.filter(is_active=True)
    lookup_url_kwarg = "item_id"

    # 這段可以不寫 然後直接用get_object() 去取得資料
    # def get_item(self, item_id):
    #     try:
    #         return Item.objects.get(id=item_id)
    #     except Item.DoesNotExist:
    #         raise Http404

    def get(self, request, item_id):  # 動態路徑所以要多收一個參數
        # 原始寫法
        # item = self.get_object()
        # serializer = self.get_serializer(item)  # 將資料轉序列化
        # return Response(serializer.data)
        return self.retrieve(request, item_id)

    def delete(self, request, item_id):  # 動態路徑所以要多收一個參數
        # item = self.get_object()
        # item.delete()
        # return Response({"massage": "Finish Delete"}, status=204)
        return self.destroy(request, item_id)

    def put(self, request, item_id):  # 動態路徑所以要多收一個參數
        # item = self.get_object()  # 取得更新物件

        # # data 前面如果有回傳值Serializer就會判定不是新建一筆而是更新
        # serializer = self.get_serializer(
        #     item, data=request.data
        # )  # 如果有傳入item 就有更新的目標（代表說是更新不是創新資料），更新內容：request.data
        # serializer.is_valid(raise_exception=True)  # 合法的話就更新
        # serializer.save()

        # return Response(serializer.data)
        return self.update(request, item_id)

    def patch(self, request, item_id):  # 只送想要更新的欄位即可
        # item = self.get_object()

        # serializer = self.get_serializer(
        #     item, data=request.data, partial=True
        # )  # partial=True 可以允許部分更新
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        # return Response(serializer.data)
        return self.partial_update(request, item_id)
"""
"""
## 版本二： 直接繼承 RetrieveUpdateDestroyAPIView
class ItemDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    lookup_url_kwarg = "item_id"
"""


## 版本三：綜合寫法
# 使用 ViewSet 就可以不用寫很多view(listView->做list DeatailView->做增刪檢查)
class ItemViewSet(ModelViewSet):
    # ModelViewSet 其實是ItemListView＋ItemDetailView這裡面的所有功能
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    pagination_class = PageNumberPagination  # 設定指定的api才有分頁
