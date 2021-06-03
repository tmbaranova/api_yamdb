# Generated by Django 3.0.5 on 2021-06-02 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20210602_1315'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='just_one_review_per_author',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='just_one_review_per_author'),
        ),
    ]