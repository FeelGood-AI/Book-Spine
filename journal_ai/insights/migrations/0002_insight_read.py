# Generated by Django 4.1.5 on 2023-02-10 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insights', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='insight',
            name='read',
            field=models.BooleanField(default=False),
        ),
    ]
