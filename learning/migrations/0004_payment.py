# Generated by Django 4.2.3 on 2023-07-24 10:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("learning", "0003_lesson_course"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
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
                ("date", models.DateField(max_length=150, verbose_name="дата оплаты")),
                ("amount", models.PositiveIntegerField(verbose_name="сумма")),
                (
                    "method",
                    models.CharField(
                        choices=[("cash", "наличные"), ("transfer", "перевод")],
                        max_length=8,
                        verbose_name="способ оплаты",
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="learning.course",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "платёж",
                "verbose_name_plural": "платежи",
            },
        ),
    ]
