<<<<<<< Updated upstream
# Generated by Django 5.0.6 on 2024-07-25 05:10
=======
# Generated by Django 5.0.6 on 2025-02-13 08:51
>>>>>>> Stashed changes

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logisticstart', '0006_alter_accounts_company_phonenumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newdeliveryschedule',
            name='receiver_number',
            field=models.IntegerField(max_length=15),
        ),
        migrations.AlterField(
            model_name='newitemlisting',
            name='recipient_phone',
            field=models.IntegerField(max_length=15),
        ),
        migrations.AlterField(
            model_name='newitemlisting',
            name='sender_phone',
            field=models.IntegerField(max_length=15),
        ),
    ]
