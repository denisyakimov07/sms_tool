# Generated by Django 3.2.9 on 2021-11-15 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('phone_number', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('last_appointment_id', models.BigIntegerField(blank=True)),
                ('last_appointment_date', models.DateTimeField(blank=True)),
                ('warning_sms_date', models.DateTimeField(blank=True, null=True)),
                ('first_sms_date', models.DateTimeField(blank=True, null=True)),
                ('second_sms_date', models.DateTimeField(blank=True, null=True)),
                ('third_sms_date', models.DateTimeField(blank=True, null=True)),
                ('one_year_sms_date', models.DateTimeField(blank=True, null=True)),
                ('final_warning_7_days_sms_date', models.DateTimeField(null=True)),
                ('cancel_by_customer', models.BooleanField(blank=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MainSetup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warning_sms', models.TextField(blank=True)),
                ('first_sms_text', models.TextField(blank=True)),
                ('second_sms_text', models.TextField(blank=True)),
                ('seven_days', models.TextField(blank=True)),
                ('zero_days', models.TextField(blank=True)),
                ('final_warning_7_days_after', models.TextField(blank=True)),
                ('update_all_users', models.BooleanField(blank=True, default=False)),
            ],
        ),
    ]
