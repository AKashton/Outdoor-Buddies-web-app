# Generated by Django 4.2.8 on 2023-12-11 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outdoorbuddies', '0003_remove_adventure_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adventureparticipants',
            name='is_host',
            field=models.BooleanField(default=False),
        ),
    ]
