# Generated by Django 3.0.5 on 2021-06-02 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210601_0916'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['username']},
        ),
    ]
