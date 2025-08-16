# 最基礎的繼承（沒有要客製化）
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser): # 建立User的model
    # 若沒有需要直接給pass就好
    # 若要客製化 
    email = models.EmailField(_("email address"), unique=True) 