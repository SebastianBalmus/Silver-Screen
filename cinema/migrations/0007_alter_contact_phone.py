# Generated by Django 4.0.6 on 2022-07-15 12:48

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0006_contact_alter_seat_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None),
        ),
    ]