
import React, { useState } from 'react';
import api from '../services/api';
import { toast } from 'react-toastify';
import './CreateProjectForm.css'; 

const CreateProjectForm = ({ onProjectCreated }) => {
    const [title, setTitle] = useState('');
    const [documentType, setDocumentType] = useState('docx');
    const [isSubmitting, setIsSubmitting] = useState(false); 

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!title.trim()) {
            toast.error('Project title cannot be empty.');
            return;
        }

        setIsSubmitting(true); 

        try {
            const response = await api.post('/projects/', {
                title: title,
                document_type: documentType,
            });
            onProjectCreated(response.data);
            setTitle('');
        } catch (err) {
            toast.error('Failed to create project. Please try again.');
            console.error(err);
        } finally {
            setIsSubmitting(false); 
        }
    };

    return (
        <div className="create-project-form-container">
            <h3>Create a New Project</h3>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="projectTitle">Project Title:</label>
                    <input
                        type="text"
                        id="projectTitle"
                        value={title}
                        onChange={(e) => setTitle(e.target.value)}
                        placeholder="e.g., Q4 Marketing Report"
                        disabled={isSubmitting} 
                    />
                </div>
                <div className="form-group">
                    <label htmlFor="documentType">Document Type:</label>
                    <select
                        id="documentType"
                        value={documentType}
                        onChange={(e) => setDocumentType(e.target.value)}
                        disabled={isSubmitting} 
                    >
                        <option value="docx">Microsoft Word (.docx)</option>
                        <option value="pptx">Microsoft PowerPoint (.pptx)</option>
                        {/* Add other document types here if needed */}
                    </select>
                </div>

                {/* --- UPDATED BUTTON --- */}
                <button
                    type="submit"
                    className={`create-project-button ${isSubmitting ? 'submitting' : ''}`}
                    disabled={isSubmitting}
                >
                    {isSubmitting ? 'Creating...' : '✨ Create Project'}
                </button>
            </form>
        </div>
    );
};

export default CreateProjectForm;