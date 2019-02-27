from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.FarmEntity)
admin.site.register(models.User_reg)
admin.site.register(models.Produce)
admin.site.register(models.Request)
admin.site.register(models.Consignment)
