import React from 'react';
import PostList from './components/PostList';
import PostForm from './components/PostForm';
import './styles/App.css';

const App = () => {
    return (
        <div>
            <PostForm />
            <PostList />
        </div>
    );
};

export default App;
