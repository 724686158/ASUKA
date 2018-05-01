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


class GitLikeModelAdmin(admin.ModelAdmin):
    pass


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'
    filter_horizontal = ('own_namespaces',)


class UserAdmin(UserAdmin):
    inlines = (EmployeeInline, )


class NamespaceAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = Namespace.objects.none()
        if hasattr(request.user, 'employee'):
            return request.user.employee.own_namespaces
        return qs


class ComponentReleaseInline(admin.TabularInline):
    model = ComponentRelease
    extra = 0


class PackageAdmin(admin.ModelAdmin):
    filter_horizontal = ('components',)
    inlines = [
        ComponentReleaseInline,
    ]

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False
        extra_context['show_save_and_continue'] = False
        return super(PackageAdmin, self).change_view(request, object_id,
                                                     form_url, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super(PackageAdmin, self).get_queryset(request)
        return qs.filter(namespace__in=request.user.employee.own_namespaces.all())

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'namespace' and hasattr(request.user, 'employee'):
            kwargs["queryset"] = Namespace.objects.filter(name__in=request.user.employee.own_namespaces.values_list('name'))
        elif not hasattr(request.user, 'employee'):
            kwargs["queryset"] = Namespace.objects.none()
        return super(PackageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if change:
            obj_orginal = self.model.objects.get(pk=obj.pk)
            obj.changed_from = obj_orginal.commit_id
            if obj_orginal.name == obj.name and obj_orginal.tag == obj.tag and obj_orginal.namespace == obj.namespace:
                obj_orginal.latest = False
                obj_orginal.save()
            obj.pk = None
            obj.save()
            rels = ComponentRelease.objects.filter(in_package=obj_orginal)
            for rel in rels:
                ComponentRelease.objects.create(component=rel.component,
                                                in_package=obj,
                                                quantity=rel.quantity)
        else:
            obj.save()


class ImageAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'namespace' and hasattr(request.user, 'employee'):
            kwargs["queryset"] = Namespace.objects.filter(name__in=request.user.employee.own_namespaces.values_list('name'))
        elif not hasattr(request.user, 'employee'):
            kwargs["queryset"] = Namespace.objects.none()
        return super(ImageAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)


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


class ComponentAdmin(admin.ModelAdmin):
    inlines = [
        EnvironmentInline,
        VolumeInline,
        PortInline,
        AffinityInline,
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'namespace' and hasattr(request.user, 'employee'):
            kwargs["queryset"] = Namespace.objects.filter(
                name__in=request.user.employee.own_namespaces.values_list('name'))
        elif not hasattr(request.user, 'employee'):
            kwargs["queryset"] = Namespace.objects.none()
        return super(ComponentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if change:
            obj_orginal = self.model.objects.get(pk=obj.pk)
            obj.changed_from = obj_orginal.commit_id
            if obj_orginal.name == obj.name and obj_orginal.tag == obj.tag and obj_orginal.namespace == obj.namespace:
                obj_orginal.latest = False
                obj_orginal.save()
            obj.pk = None
            obj.save()
            vols = Volume.objects.filter(component=obj_orginal)
            for vol in vols:
                vol.component = obj
                vol.pk = None
                vol.save()
            envs = Environment.objects.filter(component=obj_orginal)
            for env in envs:
                env.component = obj
                env.pk = None
                env.save()
            ports = Port.objects.filter(component=obj_orginal)
            for port in ports:
                port.component = obj
                port.pk = None
                port.save()
            affs = Affinity.objects.filter(component=obj_orginal)
            for aff in affs:
                aff.component = obj
                aff.pk = None
                aff.save()
        else:
            obj.save()


# Register your models here.
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Namespace, NamespaceAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Component, ComponentAdmin)