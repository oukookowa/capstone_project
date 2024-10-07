# Generated by Django 4.2.16 on 2024-10-07 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posts', '0002_post_image_post_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('original_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reposts', to='posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reposts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
