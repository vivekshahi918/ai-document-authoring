// frontend/src/services/api.js

import axios from 'axios';

const api = axios.create({
    baseURL: process.env.REACT_APP_API_BASE_URL 
    // baseURL: 'http://127.0.0.1:8000/api/v1',
     || 'https://ai-document-authoring-production.up.railway.app/api/v1',
    timeout: 0,
    // headers: {
    //     'Content-Type': 'application/json',
    // }
});

// Request Interceptor: Adds the auth token to every outgoing request's header.
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default api;
