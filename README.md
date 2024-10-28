# Blaqee API Documentation
## version: 1.0.0

## Overview
This API provides social media functionality, allowing users to create post, like, comment, repost, send & recieve direct message, recieve notification when a user reacts to a post or sends a message, and tag content. The API leverages on custom predefined tags, ensuring that each post is related to a tag. This is intended to help in organizing the posts in categories that are essential to improve user experience by targeting an all-in-one social media app - bundling jobs, photos/videos, text blogs, etc together. Users can follow and mention each other on their post and view trending posts. You can fork the project and let's build this together!

## Base URL
`<oukookowa.pythonanywhere.com>`

## Authentication
All endpoints require authentication unless otherwise specified. Please authenticate by including a token in the headers:
    `Authorization: Bearer <token>`

## Endpoints Overview

### Register a New User
- **URL**: `/api/accounts/register/`
- **Method**: `POST`
- **Description**: Registers a new user with required details (e.g., `username`, `email`, `password`).
- **Request Body**:
  ```json
  {
    "username": "exampleuser",
    "email": "user@example.com",
    "password": "password123"
  }
```
- **Response**: Returns a success message and user details upon successful registration.

### User Login
- **URL**: `/api/accounts/login/`
- **Method**: `POST`
- **Description**: Authenticates a user and returns an authentication token.
- **Request Body**:
  ```json
  {
    "username": "exampleuser",
    "password": "password123"
  }
```
- **Response**: Returns an authentication token for subsequent requests.

### View and Update User Profile
- **URL**: `/api/accounts/profile/`
- **Method**: `GET, PUT`
- **Description**: Retrieves or updates the current user's profile information
- **Response**: Returns user profile data.

### Follow a User
- **URL**: `/api/accounts/follow/<int:user_id>/`
- **Method**: `POST`
- **Description**: Follows a user with the specified user_id.
- **Response**: Returns a success message confirming the follow action.

### Unfollow a User
- **URL**: `/api/accounts/unfollow/<int:user_id>/`
- **Method**: `POST`
- **Description**: Unollows a user with the specified user_id.
- **Response**: Returns a success message confirming the unfollow action.

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
- **Create Comment**: `POST /api/comments/` (must be linked to a post)
- **Retrieve Comments**: `GET /api/comments/`
- **Retrieve Comment by ID**: `GET /api/comments/{id}/`
- **Update Comment**: `PUT /api/comments/{id}/` (Author only)
- **Delete Comment**: `DELETE /api/comments/{id}/` (Author only)

### Feed Endpoint
- **User Feed**: `GET /api/feed/`

### Conversation Endpoints
- **Create Conversation**: `POST /api/conversations/`
- **Retrieve Conversations**: `GET /api/conversations/` (participant only)
- **Retrieve Conversation by ID**: `GET /api/conversations/{id}/` (participant only)
- **Update Conversation**: `PUT /api/conversations/{id}/` (participant only)
- **Delete Conversation**: `DELETE /api/conversations/{id}/` (participant only)

### Message Endpoints
- **Create Message**: `POST /api/message/` (must be linked to a conversation)
- **Retrieve Messages**: `GET /api/message/` (participant only)
- **Retrieve Message by ID**: `GET /api/message/{id}/` (participant only)
- **Update Message**: `PUT /api/message/{id}/` (participant only)
- **Delete Message**: `DELETE /api/message/{id}/` (participant only)

### Notification Endpoint
- **Retrieve notifications**: `GET /api/notifications/` (recipient only)


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
```

## Error Codes
- **400**: Bad Request — The request could not be understood or was missing required parameters.
- **401**: Unauthorized — Authentication failed or user does not have permissions.
- **403**: Forbidden — Authentication succeeded, but authenticated user does not have access to the resource.
- **404**: Not Found — The requested resource could not be found.
- **500**: Server Error — An error occurred on the server.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.