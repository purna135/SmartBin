from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Bin)
admin.site.register(models.Garbage)