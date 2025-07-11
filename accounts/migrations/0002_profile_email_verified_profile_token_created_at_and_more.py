# Generated by Django 5.2.3 on 2025-07-01 14:16

import datetime
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='token_created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2025, 7, 1, 14, 16, 47, 713350, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='verification_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
