from rest_framework import serializers

from server.apps.playground.models import Item, ItemComment


# 要讀出comments裡面的資料不只是單獨呈現[1,2]
class ItemCommentInItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemComment
        fields = ("id", "content", "created_at", "updated_at")


class ItemWithCommentsSerializer(serializers.ModelSerializer):
    comments = ItemCommentInItemSerializer(
        read_only=True,  # 因為這個ItemSerializer同時被新增更新使用，但他們不需要呈現，所以才讓他read_only
        many=True,  # 表示說可以呈現多筆
    )

    # serializers.ModelSerializer這裡改用從model裡面傳進資料庫的值
    class Meta:
        model = Item
        fields = (  # 如果有多欄位就在這增加
            "id",
            "name",
            "description",
            "is_active",
            "comments",  # 如果要指定格式就要特別寫一個ItemCommentInItemSerializer 不然原本的長相是[1,2]
        )


class ItemSerializer(serializers.ModelSerializer):
    # serializers.ModelSerializer這裡改用從model裡面傳進資料庫的值
    class Meta:
        model = Item
        fields = (  # 如果有多欄位就在這增加
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


class ItemCommentSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(
        source="item",  # 決定要寫進的哪一個欄位 寫入的時候item_id->寫入item欄位
        queryset=Item.objects.all(),
        write_only=True,  # 只在寫入的時候出現 讀出資料的時候不需要
    )
    item = ItemSerializer(read_only=True)

    class Meta:
        model = ItemComment
        fields = ("id", "content", "item", "item_id", "created_at", "updated_at")
