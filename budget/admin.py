from typing import Any

from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html

from .models import Budget, Category, Payment
from .utils import currency_convert


class PaymentAdminInline(admin.TabularInline):
    model = Payment
    extra = 1


class BudgetAdmin(admin.ModelAdmin):
    inlines = (PaymentAdminInline,)

    change_list_template = "admin/budget/budget_change_list.html"

    list_display = (
        "category",
        "name",
        "get_estimated_amount",
        "get_actual_amount",
        "get_total_paid",
        "get_balance",
        "get_payments",
    )
    list_display_links = ("name",)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return self.model.objects.prefetch_related("payment_set").order_by(
            "category__order"
        )

    @admin.display(description="Estimated Amount")
    def get_estimated_amount(self, obj):
        return currency_convert(obj.estimated_amount)

    @admin.display(description="Actual Amount")
    def get_actual_amount(self, obj):
        val = currency_convert(obj.actual_amount)
        return format_html(f"<strong>{val}</strong>")

    @admin.display(description="Total Paid")
    def get_total_paid(self, obj):
        val = currency_convert(obj.total_paid)
        return format_html(f"<strong class='text-primary'>{val}</strong>")

    @admin.display(description="Balance")
    def get_balance(self, obj):
        if obj.balance:
            val = currency_convert(obj.balance)
            return format_html(f"<strong class='text-warning'>{val}</strong>")
        return "-"

    @admin.display(description="Payments")
    def get_payments(self, obj):
        if not obj.payments:
            return ""
        payments_list = [
            f"""<tr style='background-color: unset;'>
                    <td class="p-0 w-25 text-right text-success"><strong>{currency_convert(p.amount)}</strong></td>
                    <td class="p-0 w-50">&nbsp;&nbsp;&nbsp;&nbsp;{p.note}</td>
                    <td class="p-0 w-25 text-right">{p.date}</td>
                </tr>"""
            for p in obj.payments
        ]
        payments_str = "".join(payments_list)
        return format_html(
            f"<table class='table table-sm table-borderless mb-0 text-secondary'>{payments_str}</table>"
        )


class CategoryAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ("name", "get_budget_count", "get_items", "order")

    def get_actions(self, request):
        actions = super().get_actions(request)
        if "delete_selected" in actions:
            del actions["delete_selected"]
        return actions

    @admin.display(description="Items")
    def get_items(self, obj):
        return list(obj.budget_set.all())

    @admin.display(description="Items Count")
    def get_budget_count(self, obj):
        return obj.budget_set.count()

    # def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
    #     return self.model.objects.all().order_by('order')


admin.site.register(Budget, BudgetAdmin)
admin.site.register(Category, CategoryAdmin)
