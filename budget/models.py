from django.db import models
from django.db.models import Sum


class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampMixin):
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    @property
    def category_estimated_cost(self):
        total = self.budget_set.aggregate(Sum("estimated_amount"))
        return total["estimated_amount__sum"]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Categories"


class Budget(TimeStampMixin):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, null=True, default=None, blank=True
    )
    estimated_amount = models.IntegerField(null=True, default=None, blank=True)
    actual_amount = models.IntegerField(null=True, default=None, blank=True)
    order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ["category__order", "order", "id"]

    @property
    def payments(self):
        return self.payment_set.all()

    @property
    def total_paid(self):
        return sum(p.amount for p in self.payments)

    @property
    def balance(self):
        if self.actual_amount:
            return self.actual_amount - self.total_paid
        return None

    def __str__(self):
        return self.name


class Payment(TimeStampMixin):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    amount = models.IntegerField()
    note = models.CharField(max_length=255, null=True, default=None, blank=True)
    date = models.DateField(null=True, default=None, blank=True)

    def __str__(self):
        return self.note + " - " + str(self.amount)

    class Meta:
        ordering = ("date",)
