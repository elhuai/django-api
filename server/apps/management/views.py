from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def hello(request):  # django 裡面的view都要接request這個參數
    return Response({"message": "Hello~123"})
