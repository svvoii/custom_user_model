# Generated by Django 5.0.6 on 2024-06-12 13:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='account',
            old_name='prfile_image',
            new_name='profile_image',
        ),
    ]
