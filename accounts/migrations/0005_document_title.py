# Generated by Django 5.1.2 on 2024-12-10 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_driver_documents_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
