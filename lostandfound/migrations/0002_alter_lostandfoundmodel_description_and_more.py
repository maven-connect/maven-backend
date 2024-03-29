# Generated by Django 4.2.1 on 2023-08-15 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lostandfound', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lostandfoundmodel',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='lostandfoundmodel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator_lostfound', to=settings.AUTH_USER_MODEL),
        ),
    ]
