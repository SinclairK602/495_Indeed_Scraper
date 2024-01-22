from django.contrib import admin

from .models import Abstract

# Register your models here.


class AbstractAdmin(admin.ModelAdmin):
    list_filter = ("pmid", "date", "label")
    list_display = ("pmid", "date", "label")


admin.site.register(Abstract, AbstractAdmin)
