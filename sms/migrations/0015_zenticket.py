# Generated by Django 3.2.9 on 2021-12-12 03:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0014_delete_feedback'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZenTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_id', models.IntegerField(blank=True, null=True)),
                ('ticket_status', models.BooleanField(blank=True, default=False)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sms.customer')),
            ],
        ),
    ]
