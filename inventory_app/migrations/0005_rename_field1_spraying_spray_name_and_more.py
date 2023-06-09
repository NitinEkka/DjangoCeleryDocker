# Generated by Django 4.1.7 on 2023-03-25 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("inventory_app", "0004_rename_field1_recipe_recipe_name_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="spraying",
            old_name="field1",
            new_name="spray_name",
        ),
        migrations.RemoveField(
            model_name="spraying",
            name="field2",
        ),
        migrations.AddField(
            model_name="spraying",
            name="spray_content",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="inventory_app.recipe",
            ),
            preserve_default=False,
        ),
    ]
