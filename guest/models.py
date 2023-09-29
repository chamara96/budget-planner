from django.db import models

from budget.models import TimeStampMixin


class Category(TimeStampMixin):
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Categories"


class Guest(TimeStampMixin):
    class Status(models.TextChoices):
        SELECTED = "SE", "Selected"
        INVITED = "IN", "Invited"
        PENDING = "PE", "Pending"
        CONFIRMED = "CO", "Confirmed"
        CANCELED = "CA", "Canceled"

    name = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, null=True, default=None, blank=True
    )
    count = models.PositiveSmallIntegerField(default=1, blank=False, null=False)
    note = models.CharField(max_length=255, null=True, default=None, blank=True)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.SELECTED
    )
    drinks = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["category__order", "order", "id"]
        verbose_name_plural = " Guest List"
