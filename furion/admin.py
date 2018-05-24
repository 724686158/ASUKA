# -*- coding: UTF-8 -*-
from django.contrib import admin
from furion.models import Service
from furion.models import Variable
from furion.models import Environment
from furion.models import Region
from furion.models import UseService
from furion.models import PartnerVariable
from furion.models import PartnerVariableInEnvironment
from furion.controls import ServiceControl
from furion.controls import VariableControl
from furion.controls import RegionControl
from furion.controls import EnvironmentControl
from furion.controls import PartnerVariableControl


class RegionAdmin(admin.ModelAdmin):
    model = Region
    control = RegionControl


class VariableInline(admin.TabularInline):
    model = Variable
    extra = 0
    fk_name = "in_service"


class ServiceAdmin(admin.ModelAdmin):
    inlines = [
        VariableInline
    ]
    model = Service
    control = ServiceControl


class UseServiceInline(admin.TabularInline):
    model = UseService
    extra = 0


class PartnerVariableInEnvironmentInline(admin.TabularInline):
    model = PartnerVariableInEnvironment
    extra = 0


class EnvironmentAdmin(admin.ModelAdmin):
    inlines = [
        UseServiceInline,
        PartnerVariableInEnvironmentInline,
    ]
    model = Environment
    control = EnvironmentControl


class PartnerVariableAdmin(admin.ModelAdmin):
    model = PartnerVariable
    control = PartnerVariableControl
    list_display = ('id', 'key', 'description')


admin.site.register(Region, RegionAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Environment, EnvironmentAdmin)
admin.site.register(PartnerVariable, PartnerVariableAdmin)

