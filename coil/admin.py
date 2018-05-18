from django.contrib import admin
from coil.models import AlchimestHook
from coil.models import FurionHook
from coil.models import History


class AlchimestHookAdmin(admin.ModelAdmin):
    model = AlchimestHook
    list_display = ('url',)


class FurionHookAdmin(admin.ModelAdmin):
    model = FurionHook
    list_display = ('url',)


class HistoryAdmin(admin.ModelAdmin):
    model = History
    list_display = ('environment_name', 'package_namespace', 'package_name', 'package_tag', 'is_success', 'download_result', 'time')

    def download_result(self, obj):
        if obj.is_success:
            return "<a href='%s' download>Download Result</a>" % (obj.result.url,)
        else:
            return "<a href='%s'>ERROR Detail</a>" % (obj.result.url,)

    download_result.allow_tags = True
    download_result.short_description = 'Download Result'



admin.site.register(AlchimestHook, AlchimestHookAdmin)
admin.site.register(FurionHook, FurionHookAdmin)
admin.site.register(History, HistoryAdmin)