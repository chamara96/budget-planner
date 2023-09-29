# Generated by Django 4.2.5 on 2023-09-29 11:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("guest", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="guest",
            options={
                "ordering": ["category__order"],
                "verbose_name_plural": " Guest List",
            },
        ),
        migrations.AddField(
            model_name="guest",
            name="drinks",
            field=models.BooleanField(default=False),
        ),
    ]
