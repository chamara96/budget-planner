from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin, messages
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.urls import path
from django.utils.html import format_html

from .models import Category, Guest


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "order")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions


class GuestAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "name",
        "count",
        "note",
        "drinks",
        "status",
        "row_actions",
    )
    list_filter = [
        "category",
        "status",
        "drinks",
    ]
    list_display_links = ("name",)
    change_list_template = "admin/guest/guest_change_list.html"
    list_per_page = 300

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "changestatus/<int:id>/<str:status>",
                self.admin_site.admin_view(self.change_status),
                name="changestatus",
            ),
        ]
        return custom_urls + urls

    def change_status(self, request, id=None, status=None):
        try:
            obj = self.model.objects.get(pk=id)
            if status in self.model.Status:
                obj.status = status
                obj.save()
                messages.success(request, "The action was performed successfully.")
            else:
                messages.warning(request, "Invalid Status")
        except self.model.DoesNotExist:
            messages.warning(request, "Not found")
        return HttpResponseRedirect("/admin/guest/guest")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        guest_list = Guest.objects.all()
        liquor_count = guest_list.filter(drinks=True).count()
        categories = Category.objects.values("name")
        status = Guest.Status.choices
        guest_list_summery = guest_list.values("category__name", "status").annotate(
            count=Sum("count")
        )
        status_sum = guest_list.values("status").annotate(count=Sum("count"))
        status_summery = [
            {
                "status": s[0],
                "count": next(
                    (item["count"] for item in status_sum if item["status"] == s[0]),
                    0,
                ),
            }
            for s in status
        ]
        status_summery.append(
            {
                "status": "ALL",
                "count": sum(item["count"] for item in guest_list_summery),
            }
        )

        summery = []
        for c in categories:
            temp = {}
            temp["category"] = c.get("name")
            temp["data"] = [
                {
                    "status": s[0],
                    "count": next(
                        (
                            item["count"]
                            for item in guest_list_summery
                            if item["category__name"] == c["name"]
                            and item["status"] == s[0]
                        ),
                        "-",
                    ),
                }
                for s in status
            ]
            temp["data"].append(
                {
                    "status": "ALL",
                    "count": sum(
                        item["count"]
                        for item in guest_list_summery
                        if item["category__name"] == c["name"]
                    ),
                }
            )

            summery.append(temp)
        extra_context.update(
            {
                "status": status,
                "guest_list_summery": summery,
                "status_summery": list(status_summery),
                "liquor_count": liquor_count,
            }
        )
        return super().changelist_view(request, extra_context)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    @admin.display(description="Action")
    def row_actions(self, obj):
        BTN_INVITED = f'<a style="margin:0 10px;" href="/admin/guest/guest/changestatus/{obj.id}/IN" class="custom-action-invited">Invited</a>'
        BTN_PENDING = f'<a style="margin:0 10px;" href="/admin/guest/guest/changestatus/{obj.id}/PE" class="custom-action-pending">Pending</a>'
        BTN_CONFIRMED = f'<a style="margin:0 10px;" href="/admin/guest/guest/changestatus/{obj.id}/CO" class="custom-action-confirmed">Confirmed</a>'
        BTN_CANCELED = f'<a style="margin:0 10px;" href="/admin/guest/guest/changestatus/{obj.id}/CA" class="custom-action-calceled">Canceled</a>'
        button_list = ""
        if obj.status == Guest.Status.SELECTED:
            button_list += BTN_INVITED + BTN_CANCELED
        if obj.status == Guest.Status.INVITED:
            button_list += BTN_PENDING + BTN_CONFIRMED + BTN_CANCELED
        if obj.status == Guest.Status.PENDING:
            button_list += BTN_CONFIRMED + BTN_CANCELED
        if obj.status == Guest.Status.CONFIRMED:
            button_list += BTN_PENDING + BTN_CANCELED
        if obj.status == Guest.Status.CANCELED:
            button_list += BTN_PENDING
        return format_html(button_list)


admin.site.register(Guest, GuestAdmin)
admin.site.register(Category, CategoryAdmin)
