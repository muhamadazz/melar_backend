# Generated by Django 5.1.7 on 2025-03-15 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default=0, max_length=15, unique=True),
            preserve_default=False,
        ),
    ]
