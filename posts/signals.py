from django.db.models.signals import post_save
from django.dispatch import receiver
import re
from . models import Post, Hashtag
from django.contrib.auth import get_user_model

User = get_user_model()  # Asking django to use the default user model in use

@receiver(post_save, sender=Post)
def parse_mentions_and_hashtags(sender, instance, **kwargs):
    content = instance.content

    # Extract mentions using regex
    mention_pattern = r'@(\w+)'
    mentions = re.findall(mention_pattern, content)
    
    # Find users that match the mentions
    mentioned_users = User.objects.filter(username__in=mentions)
    instance.mentions.set(mentioned_users)

    # Extract hashtags using regex
    hashtag_pattern = r'#(\w+)'
    hashtags = re.findall(hashtag_pattern, content)
    
    # Find or create hashtags
    hashtag_objects = []
    for tag in hashtags:
        hashtag_obj, created = Hashtag.objects.get_or_create(name=tag)
        hashtag_objects.append(hashtag_obj)
    instance.hashtags.set(hashtag_objects)