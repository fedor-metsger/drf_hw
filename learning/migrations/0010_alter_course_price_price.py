# Generated by Django 4.2.3 on 2023-07-27 06:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0009_course_price_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="price",
            field=models.PositiveIntegerField(
                blank=True, default=0, null=True, verbose_name="цена"
            ),
        ),
        migrations.CreateModel(
            name="Price",
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
                ("price_id", models.CharField(max_length=50, verbose_name="id")),
                ("amount", models.PositiveIntegerField(verbose_name="сумма")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="learning.product",
                    ),
                ),
            ],
            options={
                "verbose_name": "цена",
                "verbose_name_plural": "цены",
            },
        ),
    ]
