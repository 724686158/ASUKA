# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf8")
from django.contrib import admin
from furion.models import UuevProducer


# Register your models here.

class UuevProducerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if obj.is_secret:
            obj.set_secret_value(obj.value)
        obj.save()


admin.site.register(UuevProducer, UuevProducerAdmin)
