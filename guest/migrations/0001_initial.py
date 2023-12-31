# Generated by Django 4.2.5 on 2023-09-29 05:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=100)),
                ("order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                "verbose_name_plural": "Categories",
                "ordering": ["order"],
            },
        ),
        migrations.CreateModel(
            name="Guest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=255)),
                ("count", models.PositiveSmallIntegerField(default=1)),
                (
                    "note",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("SE", "Selected"),
                            ("IN", "Invited"),
                            ("PE", "Pending"),
                            ("CO", "Confirmed"),
                            ("CA", "Canceled"),
                        ],
                        default="SE",
                        max_length=2,
                    ),
                ),
                ("order", models.PositiveSmallIntegerField(default=0)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="guest.category",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Guest List",
                "ordering": ["order"],
            },
        ),
    ]
