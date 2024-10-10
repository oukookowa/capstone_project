from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import Notification
from posts.models import Post, Comment, Like
from messages.models import Message


'''
Signal reciever for the like model which is triggered when a user likes a post
'''
@receiver(post_save, sender=Like)
def send_like_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post  # Get the post instance related to the like
        author = post.author  # Post has an author field (ForeignKey to User)
        liker = instance.user # Like model has a user field (the person who liked)

        # Create the notification
        Notification.objects.create(
            recipient=author,
            actor=liker,
            verb=f"{liker.username}liked your post",
            target_content_type=ContentType.objects.get_for_model(Like),
            target_object_id=instance.id,
        )

'''
Signal receiver for the comment model to deliver signals when a user comments on a post
'''
@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        post = instance.post  # Get the post instance related to the comment
        author = post.author  # Post model has an author field (ForeignKey to User)
        commenter = instance.author  # Comment model has a author field

        # Create the notification
        Notification.objects.create(
            recipient=author,
            actor=commenter,
            verb=f"{commenter.username} commented on your post",
            target_content_type=ContentType.objects.get_for_model(Comment),
            target_object_id=instance.id,
        )

'''
Signal receiver for the message model to deliver signal when a user sends a message
'''
@receiver(post_save, sender=Message)
def create_message_notification(sender, instance, created, **kwargs):
    if created:
        conversation = instance.conversation # Get the conversation instance related to the message
        sender = instance.sender
        # Get the conversation participants except the sender
        participants = conversation.participants.exclude(id=sender.id)
        
        # Create a notification for each participant (recipient)
        for recipient in participants:
            Notification.objects.create(
                recipient=recipient,
                actor=sender,
                verb=f"{sender.username}sent you a message",
                target_content_type=ContentType.objects.get_for_model(Message),
                target_object_id=instance.id,
            )