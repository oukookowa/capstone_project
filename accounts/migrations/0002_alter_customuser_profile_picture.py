# Generated by Django 4.2.16 on 2024-10-01 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default='profile_photos/default_photo.png', upload_to='accounts/profile_photos/'),
        ),
    ]