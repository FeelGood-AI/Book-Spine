# Generated by Django 4.1.5 on 2023-02-08 22:50

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Prompt',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=500)),
                ('date', models.DateField()),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
