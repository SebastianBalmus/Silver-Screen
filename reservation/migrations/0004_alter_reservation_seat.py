# Generated by Django 4.0.6 on 2022-08-08 17:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0013_alter_schedule_cinema_alter_schedule_hall_and_more'),
        ('reservation', '0003_alter_reservation_seat'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='seat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.seat'),
        ),
    ]
