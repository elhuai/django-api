from django.contrib import admin

# Register your models here.
from server.apps.playground.models import Item

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("name","is_active")
    list_fliter = ("is_active",) #這個,要記得加 不然執行不會過