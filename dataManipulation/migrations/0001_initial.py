# Generated by Django 2.2 on 2020-07-28 18:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(blank=True, max_length=255)),
                ('File', models.FileField(upload_to='documents//%Y/%m/%d/')),
            ],
        ),
    ]
