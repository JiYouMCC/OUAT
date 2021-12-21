# Generated by Django 4.0 on 2021-12-21 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='message_type',
            field=models.CharField(choices=[('SYS', 'System'), ('CHA', 'Chat')], default='CHA', max_length=3),
        ),
    ]
