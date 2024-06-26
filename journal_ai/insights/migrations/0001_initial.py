# Generated by Django 4.1.5 on 2023-02-10 07:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('memoirs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Insight',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=2000)),
                ('release_timestamp', models.DateTimeField()),
                ('helpful', models.BooleanField(null=True)),
                ('journaler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('memoir', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='memoirs.memoir')),
            ],
        ),
    ]
