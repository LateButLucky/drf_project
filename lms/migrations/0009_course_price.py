# Generated by Django 5.0.7 on 2024-08-11 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0008_payment"),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
