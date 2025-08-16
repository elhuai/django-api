# 最基礎的繼承（沒有要客製化）
# 如果出現Import "django.contrib.auth.models" could not be resolved from
# 代表vscode沒有啟動虛擬環境 所以要到下方環境中選擇 3.13.6(django-api)
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# 通常都預設 class User (大多習慣直接叫model User)
class User(AbstractUser):  # 建立User的model
    # 若沒有需要直接給pass就好
    # 若要客製化
    email = models.EmailField(_("email address"), unique=True)
    # email2 = models.EmailField(_("email address"), blank=True)
    # is_auth = models.BooleanField(blank=True)
