# Generated by Django 5.0.6 on 2024-07-15 08:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logisticstart', '0002_alter_newwarehouselisting_account_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newitemlisting',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='logisticstart.accounts'),
        ),
    ]
