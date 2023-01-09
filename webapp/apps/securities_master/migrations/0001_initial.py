# Generated by Django 4.1.4 on 2023-01-09 01:54
import uuid

import django.db.models.deletion
from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataVendor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('website_url', models.CharField(blank=True, max_length=255, null=True)),
                ('support_email', models.CharField(blank=True, max_length=255, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
            ],
        ),
        migrations.CreateModel(
            name='Exchange',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('abbrev', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('currency', models.CharField(blank=True, max_length=64, null=True)),
                ('timezone_offset', models.TimeField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
            ],
        ),
        migrations.CreateModel(
            name='Symbol',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ticker', models.CharField(max_length=32)),
                ('instrument', models.CharField(max_length=64)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('sector', models.CharField(blank=True, max_length=255, null=True)),
                ('currency', models.CharField(blank=True, max_length=32, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
                ('exchange', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='securities_master.exchange')),
            ],
        ),
        migrations.CreateModel(
            name='DailyPrice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('price_date', models.DateTimeField(verbose_name='price date')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
                ('last_updated_date', models.DateTimeField(auto_now=True, verbose_name='last updated date')),
                ('open_price', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('high_price', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('low_price', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('close_price', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('adj_close_price', models.DecimalField(blank=True, decimal_places=4, max_digits=19, null=True)),
                ('volume', models.BigIntegerField(blank=True, null=True)),
                ('data_vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='securities_master.datavendor')),
                ('symbol', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='securities_master.symbol')),
            ],
        ),
    ]