# Generated by Django 5.0.6 on 2024-07-24 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logisticstart', '0005_newdeliveryschedule_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='company_phonenumber',
            field=models.IntegerField(max_length=15),
        ),
    ]
