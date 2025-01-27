# Generated by Django 3.2.6 on 2022-10-12 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customAdmin', '0010_alter_employee_birthdate'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrimaryEmergencyContacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150)),
                ('relationship', models.CharField(blank=True, max_length=50)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('employee_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customAdmin.employee')),
            ],
        ),
    ]
