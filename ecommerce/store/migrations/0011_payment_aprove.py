# Generated by Django 5.0.3 on 2024-04-23 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='aprove',
            field=models.BooleanField(default=False),
        ),
    ]
