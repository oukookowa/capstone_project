# Generated by Django 4.2.16 on 2024-10-07 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_repost'),
    ]

    operations = [
        migrations.AddField(
            model_name='repost',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
