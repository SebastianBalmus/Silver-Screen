# Generated by Django 4.0.6 on 2022-07-22 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_cinema'),
    ]

    operations = [
        migrations.CreateModel(
            name='CinemaHall',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('number_of_seats', models.IntegerField()),
                ('description', models.CharField(max_length=300)),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='halls', to='cinema.cinema')),
            ],
        ),
    ]