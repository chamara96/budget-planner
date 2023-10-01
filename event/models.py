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


class SubCategory(TimeStampMixin):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, null=True, default=None, blank=True
    )
    order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.category.name + " - " + self.name

    class Meta:
        ordering = ["order"]
        verbose_name_plural = "Sub Categories"


class Task(TimeStampMixin):
    class Status(models.TextChoices):
        NONE = "NO", "-"
        STARTED = "ST", "Started"
        PENDING = "PE", "Pending"
        COMPLETED = "CO", "Completed"
        CANCELED = "CA", "Canceled"

    sub_category = models.ForeignKey(
        SubCategory, on_delete=models.DO_NOTHING, null=True, default=None, blank=True
    )
    name = models.CharField(max_length=255)
    note = models.TextField(blank=True, null=True, default=None)
    estimated_date = models.DateField(null=True, default=None, blank=True)
    actual_date = models.DateField(null=True, default=None, blank=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.NONE)
    order = models.PositiveSmallIntegerField(default=0, blank=False, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["order"]
        verbose_name_plural = " Tasks"
