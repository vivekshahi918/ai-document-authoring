// frontend/src/services/api.js

import axios from 'axios';

const api = axios.create({

    baseURL: process.env.REACT_APP_API_BASE_URL || 'http://127.0.0.1:8000/api/v1',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});

// Request Interceptor: Adds the auth token to every outgoing request's header.
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            // If a token exists, add it to the Authorization header.
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        // Handle request errors.
        return Promise.reject(error);
    }
);

export default api;