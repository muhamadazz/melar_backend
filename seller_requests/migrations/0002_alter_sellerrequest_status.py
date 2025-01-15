# Generated by Django 5.1.3 on 2024-11-27 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller_requests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerrequest',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending', max_length=10),
        ),
    ]
