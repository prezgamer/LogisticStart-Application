# Generated by Django 5.0.6 on 2024-06-20 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logisticstart', '0020_accounts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='company_phonenumber',
            field=models.CharField(max_length=15),
        ),
    ]
