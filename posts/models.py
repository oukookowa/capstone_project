from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model() # Retrieve the auth_user model being used by django

# Post model allowing users to create posts
class Post(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    content = models.TextField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)
    video = models.FileField(upload_to='posts/videos/', blank=True, null=True)
    mentions = models.ManyToManyField(User, related_name='mentioned_in', blank=True) # Allows users to mention other users starting with @<user>
    hashtags = models.ManyToManyField('Hashtag', related_name='posts', blank=True) # Allows users to relate posts to hashtag(s) starting with #<hastag name>
    tags = TaggableManager()

    # Track the count of likes associated with a post instance
    def likes_count(self):
        return self.likes.count()

    # Track the count of reposts associated with a post instance
    def reposts_count(self):
        return self.reposts.count()

    # Function to track the count of comments a post has
    @property
    def comments_count(self):
        return self.comments.count()

    def __str__(self):
        return f"{self.content[:25]} by {self.author}"

class Repost(models.Model):
    original_post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reposts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reposts')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} reposted {self.original_post.author.username}'s post"

# Comment model for users to add comment to post
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.content[:20]} by {self.author}"

# Like model to enhance user experience by allowing user to like a post
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Prevent multiple likes from the same user on the same post

    def __str__(self):
        return f"{self.post[:20]} liked by {self.user}"
    
# Model allows for the creation and tracking of hashtags
class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"#{self.name}"