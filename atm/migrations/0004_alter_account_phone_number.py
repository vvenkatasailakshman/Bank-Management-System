# Generated by Django 5.1.3 on 2024-12-04 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atm', '0003_account_otp_account_otp_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phone_number',
            field=models.PositiveBigIntegerField(),
        ),
    ]
