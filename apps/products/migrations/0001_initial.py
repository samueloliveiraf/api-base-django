# Generated by Django 5.1.4 on 2024-12-27 14:09

import django.db.models.deletion
import django.utils.timezone
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=True)),
                ('name', models.CharField(max_length=2048)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='products', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Produto',
                'verbose_name_plural': 'Produtos',
                'db_table': 'products',
                'ordering': ['-created_at'],
            },
        ),
    ]
