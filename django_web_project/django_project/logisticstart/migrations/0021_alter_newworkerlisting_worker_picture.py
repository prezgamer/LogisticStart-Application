# Generated by Django 5.0.6 on 2024-06-16 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logisticstart', '0020_alter_newworkerlisting_worker_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newworkerlisting',
            name='worker_picture',
            field=models.ImageField(default='images/null.jpg', upload_to='images/'),
        ),
    ]
