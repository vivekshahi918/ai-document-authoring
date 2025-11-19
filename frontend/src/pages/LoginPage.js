// frontend/src/pages/LoginPage.js - UPDATED

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { toast } from 'react-toastify'; // <-- IMPORT toast

import './AuthPage.css';
import logo from '../assets/logo.png';

const LoginPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [hoverState, setHoverState] = useState('default');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        const params = new URLSearchParams();
        params.append('username', email);
        params.append('password', password);

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/login', params);

            const token = response.data.access_token;
            localStorage.setItem('token', token);

            toast.success('Login Successful!'); // <-- SUCCESS notification

            // Redirect to the dashboard after a short delay
            setTimeout(() => {
                navigate('/dashboard');
            }, 2000); // 2-second delay

        } catch (error) {
            const errorMessage = error.response?.data?.detail || 'Login failed. Please check your credentials.';
            toast.error(errorMessage); // <-- ERROR notification
            console.error('Login failed!', error);
        }
    };

    return (
        <div className="auth-page-wrapper">
            <div
                className={`container ${hoverState}`}
                onMouseLeave={() => setHoverState('default')}
            >
                <div className="left-side" onMouseEnter={() => setHoverState('black')}>
                    <img src={logo} alt="Platform Logo" />
                    <h3>Welcome Back!</h3>
                </div>
                <div
                    className="right-side card"
                    onMouseEnter={() => setHoverState('glow')}
                >
                    <div className="square">
                        <i></i><i></i><i></i><i></i><i></i><i></i>
                    </div>
                    <h2>Login</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="inputBx">
                            <input type="email" placeholder="Email-Id" required value={email} onChange={(e) => setEmail(e.target.value)} />
                        </div>
                        <div className="inputBx">
                            <input type="password" placeholder="Password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                        </div>
                        <div className="inputBx">
                            <input type="submit" value="Login" />
                        </div>
                    </form>
                    {/* The message state is no longer needed here */}
                    <div className="links">
                        <p>New User? <Link to="/register">Signup Now</Link></p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;