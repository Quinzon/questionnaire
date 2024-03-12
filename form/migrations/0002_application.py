# Generated by Django 5.0.3 on 2024-03-09 11:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("form", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
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
                ("status", models.BooleanField(default=False)),
                ("email", models.EmailField(max_length=254)),
                ("json_data", models.JSONField()),
                (
                    "form",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="form.form"
                    ),
                ),
            ],
        ),
    ]