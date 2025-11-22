

import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { toast } from 'react-toastify'; 
import api from '../services/api';
import CreateProjectForm from '../components/CreateProjectForm';
import './DashboardPage.css';

const DashboardPage = () => {
    const [projects, setProjects] = useState([]);
    const [loading,setLoading] = useState(true);
    const [error, setError] = useState('');
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                setLoading(true);
                const response = await api.get('/projects/');
                setProjects(response.data);
                setError('');
            } catch (err) {
                setError('Failed to fetch projects. Your session may have expired.');
                toast.error('Failed to fetch projects. Please log in again.');
                console.error(err);
                if (err.response && err.response.status === 401) {
                    localStorage.removeItem('token');
                    setTimeout(() => navigate('/login'), 2000);
                }
            } finally {
                setLoading(false);
            }
        };
        fetchProjects();
    }, [navigate]); 

    const handleLogout = () => {
        localStorage.removeItem('token');
        toast.success('Logout Successful!');

        setTimeout(() => {
            navigate('/login');
        }, 2000); 
    };

    const handleProjectCreated = (newProject) => {
        setProjects([newProject, ...projects]);
        toast.success(`Project "${newProject.title}" created successfully!`);
    };

    return (
        <div className="dashboard-container">
            <div className="dashboard-header">
                <h1>Dashboard</h1>
                <button onClick={handleLogout} className="logout-button">Logout</button>
            </div>

            <hr style={{ width: '100%', marginBottom: '20px' }} />

            <CreateProjectForm onProjectCreated={handleProjectCreated} />

            <h2 style={{ marginTop: '40px' }}>Existing Projects</h2>
            {loading && <p>Loading projects...</p>}
            {error && !loading && <p style={{ color: 'red' }}>{error}</p>}

            {!loading && !error && (
                <div>
                    {projects.length > 0 ? (
                        <ul style={{ listStyle: 'none', padding: 0 }}>
                            {projects.map(project => (
                                <Link
                                    to={`/editor/${project.id}`}
                                    key={project.id}
                                    style={{ textDecoration: 'none', color: 'inherit' }}
                                >
                                    <li className="project-list-item">
                                        <strong>{project.title}</strong> ({project.document_type})
                                    </li>
                                </Link>
                            ))}
                        </ul>
                    ) : (
                        <p>You have no projects yet. Create one to get started!</p>
                    )}
                </div>
            )}
        </div>
    );
};

export default DashboardPage;