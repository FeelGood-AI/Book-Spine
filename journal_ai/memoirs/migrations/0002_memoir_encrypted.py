# Generated by Django 4.1.5 on 2023-04-13 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('memoirs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memoir',
            name='encrypted',
            field=models.BooleanField(default=False),
        ),
    ]
