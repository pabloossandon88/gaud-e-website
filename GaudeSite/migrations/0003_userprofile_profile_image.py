# Generated by Django 5.0.6 on 2024-06-06 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GaudeSite', '0002_alter_userprofile_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
