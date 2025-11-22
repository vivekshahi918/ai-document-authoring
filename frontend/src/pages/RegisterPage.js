
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import api from '../services/api';
import { toast } from 'react-toastify'; 

import './AuthPage.css';
import logo from '../assets/logo.png';

const RegisterPage = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [hoverState, setHoverState] = useState('default');
    const navigate = useNavigate(); 

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await api.post('/auth/register', {
            email: email,
            password: password
            });

            toast.success(`Registration successful for ${response.data.email}! Please log in.`); // <-- SUCCESS notification

        
            setTimeout(() => {
                navigate('/login');
            }, 2000); 

        } catch (error) {
            const errorMessage = error.response?.data?.detail || 'An unexpected error occurred. Please try again.';
            toast.error(errorMessage); 
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