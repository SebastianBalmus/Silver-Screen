# Generated by Django 4.0.6 on 2022-07-24 19:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0006_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='cinema',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cinema.cinema'),
            preserve_default=False,
        ),
    ]
