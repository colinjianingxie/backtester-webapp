# Generated by Django 4.1.4 on 2023-01-14 22:36

import django.contrib.postgres.fields
from django.db import migrations, models
import jsonfield.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Backtest',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('symbol_list', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=15)),
                ('initial_capital', models.DecimalField(blank=True, decimal_places=4, max_digits=20, null=True)),
                ('heartbeat', models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True)),
                ('data_handler', models.CharField(max_length=200)),
                ('execution_handler', models.CharField(max_length=200)),
                ('portfolio', models.CharField(max_length=200)),
                ('strategy_parameters', jsonfield.fields.JSONField(default={})),
                ('data_start_date', models.DateTimeField(verbose_name='data start date')),
                ('data_end_date', models.DateTimeField(verbose_name='data end date')),
                ('portfolio_start_date', models.DateTimeField(verbose_name='portfolio start date')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
            ],
        ),
        migrations.CreateModel(
            name='BacktestResult',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('events', jsonfield.fields.JSONField(default={})),
                ('total_return', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sharpe_ratio', models.DecimalField(decimal_places=2, max_digits=8)),
                ('max_drawdown', models.DecimalField(decimal_places=2, max_digits=8)),
                ('drawdown_duration', models.DecimalField(decimal_places=2, max_digits=8)),
                ('signals', models.IntegerField()),
                ('orders', models.IntegerField()),
                ('fills', models.IntegerField()),
                ('status', models.CharField(max_length=200)),
                ('start_simulation_time', models.DateTimeField(verbose_name='start_simulation_time')),
                ('end_simulation_time', models.DateTimeField(verbose_name='end_simulation_time')),
                ('duration', models.DurationField()),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='created date')),
            ],
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('strategy_parameters', jsonfield.fields.JSONField(default={})),
                ('strategy_defaults', jsonfield.fields.JSONField(default={})),
                ('strategy_min', jsonfield.fields.JSONField(default={})),
                ('strategy_max', jsonfield.fields.JSONField(default={})),
                ('use_ml', models.BooleanField(default=False)),
            ],
        ),
    ]
