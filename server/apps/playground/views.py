from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from server.apps.playground.models import Item
from server.apps.playground.serializers import ItemSerializer


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

        return Response({"status": "OK"}, status=201)


# GET /xxxxxx/items/<id> => 得到資料庫中指定的 Items
class ItemDetailView(APIView):
    def get(self, reqiuest, item_id):  # 動態路徑所以要多收一個參數
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise Http404

        serializer = ItemSerializer(item)  # 將資料轉序列化
        return Response(serializer.data)

    def delete(self, reqiuest, item_id):  # 動態路徑所以要多收一個參數
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            raise Http404

        item.delete()
        return Response({"massage": "Finish Delete"}, status=204)
