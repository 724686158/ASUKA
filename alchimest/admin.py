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
from alchimest.models import UniversallyUniqueVariable
from alchimest.models import UniversallyUniqueVariableInPackage
from alchimest.models import UniversallyUniqueVariableInComponent
from alchimest.models import Replica
from alchimest.controls import GitLikeModelControl
from alchimest.controls import ImageControl
from alchimest.controls import ComponentControl
from alchimest.controls import PackageControl
from alchimest.controls import UniversallyUniqueVariableControl
from alchimest.controls import UniversallyUniqueVariableInPackageControl
from alchimest.controls import ReplicaControl

from rest_framework.exceptions import ValidationError
from django.contrib import messages

import os

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
    model = GitLikeModel
    control = GitLikeModelControl

    search_fields = ['name']

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
    list_display = ('namespace', 'name', 'tag', 'latest', 'glm_tree')

    def glm_tree(self, obj):
        return "<a href='/alchimest/glm_tree/image/{}'>{}</a>".format(obj.name, 'glm_tree')
    glm_tree.allow_tags = True
    glm_tree.short_description = 'SHOW_IN_TREE'


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


class UniversallyUniqueVariableInComponentInline(admin.TabularInline):
    model = UniversallyUniqueVariableInComponent
    extra = 0


class ComponentAdmin(GitLikeModelAdmin):
    inlines = [
        EnvironmentInline,
        VolumeInline,
        PortInline,
        AffinityInline,
        UniversallyUniqueVariableInComponentInline,
        # UniversallyUniqueVariableInline,
    ]

    model = Component
    control = ComponentControl

    list_display = ('namespace', 'name', 'tag', 'latest', 'glm_tree')

    def glm_tree(self, obj):
        return "<a href='/alchimest/glm_tree/component/{}'>{}</a>".format(obj.name, 'glm_tree')
    glm_tree.allow_tags = True
    glm_tree.short_description = 'SHOW_IN_TREE'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'image' and hasattr(request.user, 'employee'):
            kwargs["queryset"] = Image.objects.filter(namespace__name__in=request.user.employee.own_namespaces.values_list('name'))
        return super(ComponentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        super(ComponentAdmin, self).save_model(request, obj, form, change)


class ComponentReleaseInline(admin.TabularInline):
    model = ComponentRelease
    extra = 0


class UniversallyUniqueVariableInPackageInline(admin.TabularInline):
    model = UniversallyUniqueVariableInPackage
    extra = 0


class PackageAdmin(GitLikeModelAdmin):
    inlines = [
        ComponentReleaseInline,
        UniversallyUniqueVariableInPackageInline,
        # UniversallyUniqueVariableInline,
    ]
    model = Package
    control = PackageControl

    list_display = ('namespace', 'name', 'tag', 'latest', 'approved', 'glm_tree')

    def glm_tree(self, obj):
        return "<a href='/alchimest/glm_tree/package/{}'>{}</a>".format(obj.name, 'glm_tree')
    glm_tree.allow_tags = True
    glm_tree.short_description = 'SHOW_IN_TREE'


class UniversallyUniqueVariableAdmin(admin.ModelAdmin):
    model = UniversallyUniqueVariable
    control = UniversallyUniqueVariableControl


class ReplicaAdmin(admin.ModelAdmin):
    model = Replica
    control = ReplicaControl
    list_display = ('id', 'time', 'user', 'create_replica', 'download_replica_file', 'ues_replica')

    def download_replica_file(self, obj):
        if obj.data_file and os.path.isfile(".{}".format(obj.data_file.url)):
            return "<a href='{}' download>Download</a>".format(obj.data_file.url)
        else:
            return "Without Replica File"
    download_replica_file.allow_tags = True
    download_replica_file.short_description = 'Download'

    def create_replica(self, obj):
        if obj.data_file and os.path.isfile(".{}".format(obj.data_file.url)):
            return "Created".format(obj.id)
        else:
            return "<a href='/alchimest/dump_data/{}'> Create Replica</a>".format(obj.id)
    create_replica.allow_tags = True
    create_replica.short_description = 'Create Replica File'

    def ues_replica(self, obj):
        if obj.data_file and os.path.isfile(".{}".format(obj.data_file.url)):
            return "<a href='/alchimest/load_data/{}'>Use Replica</a>".format(obj.id)
        else:
            return "Without Replica File"

    ues_replica.allow_tags = True
    ues_replica.short_description = 'USE REPLICA'

#
# class UniversallyUniqueVariableInPackageAdmin(admin.ModelAdmin):
#     model = UniversallyUniqueVariableInPackage
#     control = UniversallyUniqueVariableInPackageControl


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Namespace, NamespaceAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(UniversallyUniqueVariable, UniversallyUniqueVariableAdmin)
admin.site.register(Replica, ReplicaAdmin)