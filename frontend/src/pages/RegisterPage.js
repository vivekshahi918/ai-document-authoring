// frontend/src/pages/RegisterPage.js - UPDATED

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; // <-- IMPORT useNavigate
import axios from 'axios';
import { toast } from 'react-toastify'; // <-- IMPORT toast

import './AuthPage.css';
import logo from '../assets/logo.png';

const RegisterPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [hoverState, setHoverState] = useState('default');
    const navigate = useNavigate(); // <-- Hook for navigation

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/register', {
                email: email,
                password: password
            });

            toast.success(`Registration successful for ${response.data.email}! Please log in.`); // <-- SUCCESS notification

            // Redirect to the login page after a short delay
            setTimeout(() => {
                navigate('/login');
            }, 2000); // 3-second delay

        } catch (error) {
            const errorMessage = error.response?.data?.detail || 'An unexpected error occurred. Please try again.';
            toast.error(errorMessage); // <-- ERROR notification
            console.error('Registration failed!', error);
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
                    <h3>Create Your Account</h3>
                </div>
                <div
                    className="right-side card"
                    onMouseEnter={() => setHoverState('glow')}
                >
                    <div className="square">
                        <i></i><i></i><i></i><i></i><i></i><i></i>
                    </div>
                    <h2>Sign Up</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="inputBx">
                            <input type="email" placeholder="Email-Id" required value={email} onChange={(e) => setEmail(e.target.value)} />
                        </div>
                        <div className="inputBx">
                            <input type="password" placeholder="Password" required value={password} onChange={(e) => setPassword(e.target.value)} />
                        </div>
                        <div className="inputBx">
                            <input type="submit" value="Sign Up" />
                        </div>
                    </form>
                    {/* The message state is no longer needed here */}
                    <div className="links">
                        <p>Already a user? <Link to="/login">Login Now</Link></p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;