# Generated by Django 4.0.6 on 2022-07-25 09:39

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0007_schedule_cinema'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schedule',
            name='hall',
            field=smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='cinema', chained_model_field='cinema', on_delete=django.db.models.deletion.CASCADE, to='cinema.cinemahall'),
        ),
    ]
