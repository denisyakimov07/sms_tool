# Generated by Django 3.2.9 on 2022-10-01 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0022_remove_emailreport_unsubscribe_status_include'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailReportRecipient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emails_list', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='emailreport',
            name='emails_list',
        ),
    ]
