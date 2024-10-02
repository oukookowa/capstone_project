from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from posts.models import Post, Comment, Like


# Signal reciever for the like model which is triggered when a user likes a post
@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post  # Post model has a ForeignKey to Post
        author = post.author  # Post has an author field (ForeignKey to User)
        liker = instance.user  # Like model has a user field (the person who liked)

        # Create the notification
        Notification.objects.create(
            recipient=author,
            actor=liker,
            verb=f"{liker.username}liked your post",
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id,
        )

# Signal receiver for the comment model to deliver signals when a user comments on a Post
@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post  # Post model has a ForeignKey to Post
        author = post.author  # Post model has an author field (ForeignKey to User)
        commenter = instance.author  # Comment model has a author field

        # Create the notification
        Notification.objects.create(
            recipient=author,
            actor=commenter,
            verb=f"{commenter.username} commented on your post",
            target_content_type=ContentType.objects.get_for_model(Post),
            target_object_id=post.id,
        )