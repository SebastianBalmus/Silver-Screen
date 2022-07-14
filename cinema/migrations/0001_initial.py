# Generated by Django 4.0.6 on 2022-07-14 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('poster', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('imdb_link', models.CharField(max_length=150)),
                ('imdb_id', models.CharField(max_length=30)),
                ('trailer_link', models.CharField(max_length=150)),
                ('length', models.CharField(max_length=10)),
            ],
        ),
    ]