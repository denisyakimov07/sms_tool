# Generated by Django 3.2.9 on 2021-12-12 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0016_zenticket_zen_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zenticket',
            name='zen_user_id',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
