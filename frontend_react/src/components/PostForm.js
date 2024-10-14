import React, { useState } from 'react';
import axios from 'axios';

const PostForm = () => {
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await axios.post('http://localhost:8000/api/posts/', { title, content });
            setTitle('');  // Clear the form after successful submission
            setContent('');
        } catch (error) {
            console.error('Error creating post:', error);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <label htmlFor="title">Title</label>
            <input
                type="text"
                id="title"             // Add id attribute
                name="title"           // Add name attribute
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="title"
                required
            />
            <label htmlFor="content">Content</label>
            <textarea
                id="content"           // Add id attribute
                name="content"         // Add name attribute
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Content"
                required
            ></textarea>
            <button type="submit">Create Post</button>
        </form>
    );
};

export default PostForm;
