# Generated by Django 4.2.1 on 2023-07-17 13:43

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0004_alter_group_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
