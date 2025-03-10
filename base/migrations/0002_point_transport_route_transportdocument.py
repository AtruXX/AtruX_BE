# Generated by Django 5.1.2 on 2025-03-09 21:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_truck', models.CharField(max_length=100)),
                ('status_truck_text', models.CharField(blank=True, max_length=255, null=True)),
                ('status_goods', models.CharField(max_length=100)),
                ('truck_combination', models.CharField(max_length=100)),
                ('status_coupling', models.CharField(max_length=100)),
                ('trailer_type', models.CharField(max_length=100)),
                ('trailer_number', models.CharField(max_length=100)),
                ('status_trailer_wagon', models.CharField(max_length=100)),
                ('status_loaded_truck', models.CharField(max_length=100)),
                ('detraction', models.CharField(max_length=100)),
                ('status_transport', models.CharField(default='not started', max_length=100)),
                ('dispatcher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dispatcher_transports', to=settings.AUTH_USER_MODEL)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_transports', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('points', models.ManyToManyField(to='base.point')),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routes', to='base.transport')),
            ],
        ),
        migrations.CreateModel(
            name='TransportDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('document', models.FileField(upload_to='transport_documents/')),
                ('category', models.CharField(blank=True, max_length=100, null=True)),
                ('transport', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='base.transport')),
            ],
        ),
    ]
