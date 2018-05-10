from django.contrib import admin
from coil.models import A
from coil.models import B

# Register your models here.
class BAdmin(admin.ModelAdmin):

    list_display = ['a', ]


class BInline(admin.StackedInline):
    model = B


class AAdmin(admin.ModelAdmin):
    inlines = [BInline, ]


admin.site.register(A, AAdmin)
admin.site.register(B, BAdmin)