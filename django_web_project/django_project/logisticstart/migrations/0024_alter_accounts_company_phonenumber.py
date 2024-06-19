# Generated by Django 5.0.6 on 2024-06-19 13:00

import logisticstart.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logisticstart', '0023_alter_accounts_company_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='company_phonenumber',
            field=models.IntegerField(validators=[logisticstart.models.validate_phone_number_length]),
        ),
    ]
