# Generated by Django 2.0.4 on 2018-04-29 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0002_auto_20180430_0009'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='renevue',
            new_name='revenue',
        ),
    ]
