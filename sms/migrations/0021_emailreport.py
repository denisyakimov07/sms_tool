# Generated by Django 3.2.9 on 2022-09-30 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0020_zenticket_creat'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.IntegerField(default=0, null=True)),
                ('unsubscribe_status_include', models.BooleanField(blank=True, default=True)),
                ('emails_list', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
