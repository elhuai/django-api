from rest_framework import serializers

from server.apps.playground.models import Item


class ItemSerializer(serializers.ModelSerializer):
    # serializers.ModelSerializer這裡改用從model裡面傳進資料庫的值
    class Meta:
        model = Item
        fields = (
            "id",
            "name",
            "description",
            "is_active",
        )

    def validate(self, attrs):
        extra_fields = set(self.initial_data.keys()) - set(self.fields.keys())
        if extra_fields:
            raise serializers.ValidationError(f"有多餘欄位: {', '.join(extra_fields)}")
        return attrs
