# Generated by Django 5.0.3 on 2024-03-31 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_rename_data_completed_order_complete_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='productcategory',
            name='slug',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='producttype',
            name='slug',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]