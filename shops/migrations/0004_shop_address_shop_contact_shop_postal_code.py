# Generated by Django 5.1.3 on 2024-12-05 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0003_remove_product_category_remove_product_is_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='address',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='contact',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shop',
            name='postal_code',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]