from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .models import Category, SubCategory, Task


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "get_sub_categories", "order")

    @admin.display(description="Sub Categories")
    def get_sub_categories(self, obj):
        return list(obj.subcategory_set.all())

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


class SubCategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "category", "order")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


class TaskAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = (
        "order",
        "get_sub_category",
        "name",
        "note",
        "estimated_date",
        "actual_date",
        "status",
    )
    list_display_links = ("name",)
    list_filter = ["sub_category__category"]

    @admin.display(description="Sub Category")
    def get_sub_category(self, obj):
        return obj.sub_category.name

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Task, TaskAdmin)
