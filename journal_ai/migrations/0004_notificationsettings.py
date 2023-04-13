# Generated by Django 4.1.5 on 2023-04-13 03:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('journal_ai', '0003_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timezoneOffset', models.CharField(max_length=100)),
                ('timezoneName', models.CharField(max_length=100)),
                ('fcmToken', models.CharField(max_length=512)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
