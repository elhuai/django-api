from django.db import models

# Create your models here.
# jango 會自動產生一個id 所以不用特別打

class Item(models.Model):
    name  = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)