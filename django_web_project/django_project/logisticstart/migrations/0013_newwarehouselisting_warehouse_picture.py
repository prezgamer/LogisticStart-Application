# Generated by Django 5.0.6 on 2024-06-16 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logisticstart', '0012_alter_newwarehouselisting_warehouse_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='newwarehouselisting',
            name='warehouse_picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='images/'),
        ),
    ]
