# Generated by Django 5.0.7 on 2024-07-25 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lms", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="preview",
            field=models.URLField(),
        ),
    ]
