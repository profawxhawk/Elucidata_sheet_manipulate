# Generated by Django 2.2 on 2020-07-29 19:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dataManipulation', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='Name',
        ),
    ]
