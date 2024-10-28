# Social Media API Documentation

## Overview
This API provides social media functionality, allowing users to create post, like, comment, repost, send direct messages, recieve notifications on posts and messages, and tag content. Users can also follow and mention each other and view trending posts. You can fork the project and let's build this together!

## Base URL
`<oukookowa.pythonanywhere.com>`

## Authentication
All endpoints require authentication unless otherwise specified. Please authenticate by including a token in the headers:
        Authorization: Bearer <token>


## Endpoints Overview
### Post Endpoints
- **Create Post**: `POST /api/posts/`
- **Retrieve Posts**: `GET /api/posts/`
- **Retrieve Post by ID**: `GET /api/posts/{id}/`
- **Update Post**: `PUT /api/posts/{id}/` (Author only)
- **Delete Post**: `DELETE /api/posts/{id}/` (Author only)
- **Like a Post**: `POST /api/posts/{id}/like/`
- **Unlike a Post**: `POST /api/posts/{id}/unlike/`
- **Repost a Post**: `POST api/posts/{id}/reposts/`
- **View Hashtag Posts**: `GET /api/posts/hashtag/{hashtag}/`
- **View Tagged Posts**: `GET /api/posts/tag/{tag}/`
- **View Mentioned Posts**: `GET /api/posts/mention/{username}/`
- **Trending Posts**: `GET /api/trending/`

### Comment Endpoints
- **Create Comment**: `POST /api/comments/`
- **Retrieve Comments**: `GET /api/comments/`

### Feed Endpoint
- **User Feed**: `GET /api/feed/`

## Example Usage
### Create a Post
```bash
curl -X POST "oukookowa.pythonanywhere.com/api/posts/" \
     -H "Authorization: Bearer <token>" \
     -d "{
           'title': 'My First Post',
           'content': 'This is the content of my post.',
           'tags': ['tag1', 'tag2']
         }"

## Error Codes

- **400**: Bad Request — The request could not be understood or was missing required parameters.
- **401**: Unauthorized — Authentication failed or user does not have permissions.
- **403**: Forbidden — Authentication succeeded, but authenticated user does not have access to the resource.
- **404**: Not Found — The requested resource could not be found.
- **500**: Server Error — An error occurred on the server.
