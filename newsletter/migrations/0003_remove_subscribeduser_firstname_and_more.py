# Generated by Django 4.0.6 on 2022-08-29 17:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletter', '0002_remove_subscribeduser_name_subscribeduser_firstname_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscribeduser',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='subscribeduser',
            name='lastname',
        ),
    ]
