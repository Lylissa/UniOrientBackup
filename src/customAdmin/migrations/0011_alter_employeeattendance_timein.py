# Generated by Django 3.2.6 on 2021-11-30 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customAdmin', '0010_employeeattendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeattendance',
            name='timein',
            field=models.TimeField(blank=True),
        ),
    ]