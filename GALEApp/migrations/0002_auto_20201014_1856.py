# Generated by Django 3.1.2 on 2020-10-14 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('GALEApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deliveries',
            old_name='match_id',
            new_name='match',
        ),
    ]
