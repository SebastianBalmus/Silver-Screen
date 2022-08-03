# Generated by Django 4.0.6 on 2022-08-01 09:55

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0010_schedule_unique_schedule'),
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='seat',
            field=smart_selects.db_fields.ChainedForeignKey(chained_field='details', chained_model_field='details__hall', on_delete=django.db.models.deletion.CASCADE, to='cinema.seat'),
        ),
    ]
