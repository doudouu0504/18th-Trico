# Generated by Django 5.1.4 on 2024-12-26 08:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("services", "0002_service_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="premium_delivery_time",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="premium_description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="premium_price",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="premium_title",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="standard_delivery_time",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="service",
            name="standard_description",
            field=models.TextField(default="Default description"),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="service",
            name="standard_price",
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="service",
            name="standard_title",
            field=models.CharField(default="Default title", max_length=100),
            preserve_default=False,
        ),
    ]
