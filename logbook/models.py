from django.db import models

from budget.models import TimeStampMixin


class Logbook(TimeStampMixin):
    lable = models.CharField(max_length=100)
    note = models.TextField(blank=False, null=False)
    date = models.DateTimeField(null=True, default=None, blank=True)

    def __str__(self):
        return self.lable

    class Meta:
        ordering = ["date"]
        verbose_name_plural = "Logbook"
