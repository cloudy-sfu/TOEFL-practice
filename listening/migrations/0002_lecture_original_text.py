# Generated by Django 5.0.1 on 2024-01-19 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listening', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='original_text',
            field=models.TextField(blank=True),
        ),
    ]
