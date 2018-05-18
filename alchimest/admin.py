from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from alchimest.models import Namespace
from alchimest.models import Image
from alchimest.models import Component
from alchimest.models import Package
from alchimest.models import Employee
from alchimest.models import ComponentRelease
from alchimest.models import Affinity
from alchimest.models import Volume
from alchimest.models import Port
from alchimest.models import Environment
from alchimest.models import GitLikeModel
from alchimest.controls import GitLikeModelControl
from alchimest.controls import ImageControl
from alchimest.controls import ComponentControl
from alchimest.controls import PackageControl
from rest_framework.exceptions import ValidationError
from django.contrib import messages

import logging

# LOG = logging.getLogger(__name__)
# LOG.addHandler(logging.FileHandler('mylog.log'))


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    filter_horizontal = ('own_namespaces',)


class UserAdmin(UserAdmin):
    inlines = [
        EmployeeInline,
    ]
    list_display = ('username', 'email', 'last_login', 'is_staff', 'is_superuser', 'get_job')

    def get_job(self, obj):
        if obj.employee:
            return obj.employee.job
        else:
            return 'without job'

    get_job.allow_tags = True
    get_job.short_description = 'JOB'

class NamespaceAdmin(admin.ModelAdmin):
    model = Namespace

    def get_queryset(self, request):

        if hasattr(request.user, 'employee'):
            return request.user.employee.own_namespaces
        else:
            return self.model.objects.none()


class GitLikeModelAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ('name', 'tag', 'namespace', 'latest')

    model = GitLikeModel
    control = GitLikeModelControl

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = self.model.objects.get(pk=obj.pk)
            if old_obj.name != obj.name:
                self.control.new(old_obj, obj)
            elif old_obj.namespace != obj.namespace:
                self.control.fork(old_obj, obj)
            elif old_obj.tag != obj.tag:
                self.control.commit(old_obj, obj)
            else:
                obj.save()
        else:
            obj.save()

    def get_queryset(self, request):
        return self.model.objects.filter(namespace__in=request.user.employee.own_namespaces.all())

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'namespace' and hasattr(request.user, 'employee'):
            kwargs["queryset"] = Namespace.objects.filter(name__in=request.user.employee.own_namespaces.values_list('name'))
        return super(GitLikeModelAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


class ImageAdmin(GitLikeModelAdmin):
    model = Image
    control = ImageControl


class AffinityInline(admin.TabularInline):
    model = Affinity
    extra = 0
    fk_name = "component"


class VolumeInline(admin.TabularInline):
    model = Volume
    extra = 0
    fk_name = "component"


class PortInline(admin.TabularInline):
    model = Port
    extra = 0
    fk_name = "component"


class EnvironmentInline(admin.TabularInline):
    model = Environment
    extra = 0
    fk_name = "component"


class ComponentAdmin(GitLikeModelAdmin):
    inlines = [
        EnvironmentInline,
        VolumeInline,
        PortInline,
        AffinityInline,
    ]

    model = Component
    control = ComponentControl

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'image' and hasattr(request.user, 'employee'):
            kwargs["queryset"] = Image.objects.filter(namespace__name__in=request.user.employee.own_namespaces.values_list('name'))
        return super(ComponentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


    def save_model(self, request, obj, form, change):

        super(ComponentAdmin, self).save_model(request, obj, form, change)


class ComponentReleaseInline(admin.TabularInline):
    model = ComponentRelease
    extra = 0


class PackageAdmin(GitLikeModelAdmin):
    list_display = ('name', 'tag', 'namespace', 'latest', 'approved')
    inlines = [
        ComponentReleaseInline,
    ]
    model = Package
    control = PackageControl


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Namespace, NamespaceAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Package, PackageAdmin)
