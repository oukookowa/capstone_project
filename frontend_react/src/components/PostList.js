// src/PostList.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const PostList = () => {
    const [posts, setPosts] = useState([]); // Initializing posts as an empty array
    const [error, setError] = useState(null); // State for error handling
    const [loading, setLoading] = useState(true); // State for loading indicator

    useEffect(() => {
        fetchPosts();
    }, []);

    const fetchPosts = async () => {
        try {
            const response = await axios.get('http://localhost:8000/api/posts/');
            console.log('API response:', response.data); // Log the API response
            
            // Assuming the posts are in response.data.posts; adjust this if your API structure is different
            setPosts(response.data); // Set posts if response is an array
        } catch (error) {
            console.error('Error fetching posts:', error);
            setError('Error fetching posts. Please try again later.'); // Set error message if API fails
        } finally {
            setLoading(false); // Set loading to false after API call
        }
    };

    // Conditional rendering for loading, error, and posts
    if (loading) {
        return <div>Loading...</div>; // Loading indicator
    }

    if (error) {
        return <div>{error}</div>; // Display error message
    }

    return (
        <div>
            <h1>Posts</h1>
            <ul>
                {Array.isArray(posts) && posts.length > 0 ? (
                    posts.map(post => (
                        <li key={post.id}>
                            <h2>{post.title}</h2>
                            <p>{post.content}</p>
                        </li>
                    ))
                ) : (
                    <li>No posts available</li> // Fallback message when no posts are present
                )}
            </ul>
        </div>
    );
};

export default PostList;
