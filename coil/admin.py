from django.contrib import admin
from coil.models import AlchimestHook
from coil.models import FurionHook
from coil.models import DeploymentRecord
from coil.controls import *
import os


class AlchimestHookAdmin(admin.ModelAdmin):
    model = AlchimestHook
    control = AlchimestHookControl
    list_display = ('url',)


class FurionHookAdmin(admin.ModelAdmin):
    model = FurionHook
    control = FurionHookControl
    list_display = ('url',)


class DeploymentRecordAdmin(admin.ModelAdmin):
    model = DeploymentRecord
    control = DeploymentRecordControl
    list_display = ('environment_name', 'package_namespace', 'package_name', 'package_tag', 'test_delpoy', 'is_success', 'download_result', 'time')

    def test_delpoy(self, obj):
        return "<a href='/coil/link_test/{}/{}/{}/{}'>{}</a>".format(obj.environment_name,
                                                                     obj.package_namespace,
                                                                     obj.package_name,
                                                                     obj.package_tag,
                                                                     'TEST_DEPLOY')
    test_delpoy.allow_tags = True
    test_delpoy.short_description = 'TEST_DEPLOY'

    def download_result(self, obj):
        if obj.result and os.path.isfile(".{}".format(obj.result.url)):
            if obj.is_success:
                return "<a href='{}' download>Download Result</a>".format(obj.result.url)
            else:
                return "<a href='{}'>Error Detail</a>".format(obj.result.url)
        else:
            return "Without Datafile "

    download_result.allow_tags = True
    download_result.short_description = 'Download Result'



admin.site.register(AlchimestHook, AlchimestHookAdmin)
admin.site.register(FurionHook, FurionHookAdmin)
admin.site.register(DeploymentRecord, DeploymentRecordAdmin)