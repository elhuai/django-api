from rest_framework import serializers

from server.apps.playground.models import Item

class ItemSerializer(serializers.ModelSerializer): # serializers.ModelSerializer這裡改用從model裡面傳進資料庫的值
    class Meta:
        model = Item
        fields = (
            "id",
            "name",
            "description",
            "is_active",
        )