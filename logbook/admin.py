from django.contrib import admin

from .models import Logbook


class LogbookAdmin(admin.ModelAdmin):
    list_display = ("lable", "note", "date")
    list_display_links = ("lable",)


admin.site.register(Logbook, LogbookAdmin)
