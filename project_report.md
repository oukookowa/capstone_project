
# Capstone Project  
**Pinto Okowa**  
**ALX SE - Back-end Engineering**  

## Project Report and Reflection

I am highly indebted to ALX Africa for the opportunity to learn such valuable skills in record time, thanks to the course structure and organization. Thanks to the BE mentors, you are my heroes today. I hope we continue this great association in the future.

I have committed tireless days and nights to this project. I want to set the path for gaining experience in the skills we have learned. My passion for tech became clear during this project. I got excited amidst the daunting challenges that come with bugs and imagining that they must be fixed for an outcome to be desirable. The desire to make every aspect of the application work according to the business logic in pursuit was real and kept refueling my constantly draining tanks.

I was inspired by the talk by one of ALX's guests, Ayida Getachew, a seasoned technical recruiter, who emphasized the power of working on one’s projects and collaborating on open-source projects. As a junior developer trying to find his way, her advice is critical to ensure I am welcome at the table.

I started the social media project by designing the **ERD diagram**. This was essential to have a clear view of the models and relationships that would be my MVP. Being new to the design of **Entity Relationship Diagrams**, I had to spend a meaningful amount of time watching explanatory videos to understand how the Lucidchart.io platform works. In the end, I had an appealing design that rewarded my devotion.

I then used **Django ORM** to implement the relationships between entities as described in the ERD diagram. There were challenges in implementing some features like the **tags**. While **Django-taggit** makes it easy to use the tags, I learned that for APIs, you had to make a stretch to ensure the data is saved with the post instance. At first, I didn’t understand why, during post creation, I’d see the tags, only for them to disappear when I tried to retrieve the post. I later learned that **taggit**, despite having the **Tag** model and its serializer, requires one to include the tag serializer in the serializer of the model where the ‘tags’ attribute is used. It also involved setting the tags data from the validated data as shown in the code snippet below:

# Post serializer to serialize a post together with comments, likes, author, reposts, mentions, hashtags, & tags associated with it
class PostSerializer(TaggitSerializer, serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = LikeSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True) 
    reposts = RepostSerializer(many=True, read_only=True)
    mentions = UserSerializer(many=True, read_only=True) 
    hashtags = HashtagSerializer(many=True, read_only=True)
    tags = TagListSerializerField() # Holds the tags associated with an instance of a post

    class Meta:
        model = Post
        fields = '__all__'

    # Associate a post with the authenticated user at the instance a post is created
    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags', [])  # Pop tags from validated data
        post = Post.objects.create(author=request.user, **validated_data) # Set author
        post.tags.set(tags)  # Add respective tags to the post instance explicitly
        return post

Finally, I ventured into the **deployment** of my app. I always like adventure. I tried **Dokku** and **Coolify**, which I found to be powerful resources, but configuring Docker properly was challenging. I got so many bugs while trying Coolify. I fixed some, but in the interest of time, I opted for **PythonAnywhere**, which, with much less hassle, allowed me to deploy my second API.

I decided to implement the **front end** of my API using **React.js**. While writing this report, I’m still trying out various aspects of React, learning the basics of the trade, and hoping that in the end, I will dress my API with a beautiful User Interface!
