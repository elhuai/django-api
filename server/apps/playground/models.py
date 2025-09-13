from django.db import models

# Create your models here.
# jango 會自動產生一個id 所以不用特別打

# 這邊有改動都要：
# 建立遷移檔 Models -> Migrations：uv run manage.py makemigrations
# 遷移檔套用到資料庫 Migrations -> DB：uv run manage.py migrate


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)


class ItemComment(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,  # CASCADE 當Item被刪除時，comment一起刪除
        related_name="comments",  # related_name 可以改取得的key值（預設 itemcomment_set）
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # 建立的時候自動加入現在日期
    updated_at = models.DateTimeField(auto_now=True)
