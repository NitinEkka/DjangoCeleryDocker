# Generated by Django 4.1.7 on 2023-03-26 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory_app", "0008_alter_drenching_status_alter_spraying_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="drenching",
            name="status",
            field=models.CharField(
                choices=[("success", "Success"), ("failure", "Failure")], max_length=10
            ),
        ),
        migrations.AlterField(
            model_name="spraying",
            name="status",
            field=models.CharField(
                choices=[("success", "Success"), ("failure", "Failure")], max_length=10
            ),
        ),
        migrations.AlterField(
            model_name="stockusage",
            name="status",
            field=models.CharField(
                choices=[("success", "Success"), ("failure", "Failure")], max_length=10
            ),
        ),
    ]
