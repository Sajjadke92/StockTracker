# Generated by Django 5.1.4 on 2024-12-11 22:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("warehouses", "0002_wein"),
    ]

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
                ("title", models.CharField(max_length=50, unique=True)),
                ("description", models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name="wein",
            name="drink_ptr",
        ),
        migrations.CreateModel(
            name="Item",
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
                ("name", models.CharField(max_length=50)),
                ("location", models.CharField(max_length=50)),
                ("quantity", models.IntegerField()),
                ("expiry", models.DateField()),
                ("updated_time", models.DateTimeField(auto_now=True)),
                ("description", models.TextField(blank=True)),
                (
                    "Category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="warehouses.category",
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Drink",
        ),
        migrations.DeleteModel(
            name="wein",
        ),
    ]