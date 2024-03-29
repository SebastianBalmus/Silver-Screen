# Generated by Django 4.0.6 on 2022-08-01 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cinema', '0010_schedule_unique_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.schedule')),
                ('seat', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='cinema.seat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
