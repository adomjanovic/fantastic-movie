# Generated by Django 2.0.4 on 2018-04-30 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App1', '0003_auto_20180430_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='gender',
            field=models.CharField(max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='actor',
            name='place_of_birth',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='director',
            name='place_of_birth',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
