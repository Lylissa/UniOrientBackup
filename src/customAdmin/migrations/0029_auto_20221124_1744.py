# Generated by Django 3.2.9 on 2022-11-24 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customAdmin', '0028_merge_20221124_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newuser',
            name='role',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]