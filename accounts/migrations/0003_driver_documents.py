# Generated by Django 5.1.2 on 2024-12-01 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_driver_on_road'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='documents',
            field=models.FileField(blank=True, null=True, upload_to='driver_documents/'),
        ),
    ]
