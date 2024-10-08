# Generated by Django 5.0.4 on 2024-09-21 09:49

import django_extensions.db.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('location', models.CharField(max_length=500)),
                ('description', models.CharField(max_length=1000)),
                ('identification', models.CharField(blank=True, max_length=300, null=True)),
                ('tamper_seal', models.CharField(blank=True, max_length=300, null=True)),
                ('overhead_sign', models.CharField(max_length=250)),
                ('checklist', models.CharField(max_length=250)),
                ('s_on_floor', models.CharField(max_length=250)),
                ('comments', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name': 'Item',
                'verbose_name_plural': 'Items',
            },
        ),
    ]
