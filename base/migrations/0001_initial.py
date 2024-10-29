# Generated by Django 5.1.2 on 2024-10-29 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('name', models.CharField(max_length=100, unique=True)),
                ('code', models.CharField(max_length=100, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]
