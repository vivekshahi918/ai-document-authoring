import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import SectionEditor from '../components/SectionEditor';
import './EditorPage.css'; 

const EditorPage = () => {
    const { projectId } = useParams();

    const [mainTopic, setMainTopic] = useState('');
    const [sections, setSections] = useState([{ title: '' }]);
    const [generatedContent, setGeneratedContent] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isExporting, setIsExporting] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        const fetchProjectDetails = async () => {
            try {
                const response = await api.get(`/projects/${projectId}`);
                const project = response.data;

                if (project.main_topic) {
                    setMainTopic(project.main_topic);
                }

                if (project.sections && project.sections.length > 0) {
                    
                    if (typeof project.sections[0] === 'object') {
                        setSections(project.sections.map(s => ({ title: s.title })));
                        
                        const hasContent = project.sections.some(s => s.content && s.content.trim() !== "");
                        if (hasContent) {
                            setGeneratedContent(project.sections);
                        }
                    } 
                    else {
                        setSections(project.sections.map(title => ({ title: title })));
                    }
                } else {
                    setSections([{ title: '' }]);
                }

            } catch (err) {
                setError("Failed to load project details. You may be offline or the project doesn't exist.");
                console.error(err);
            }
        };

        fetchProjectDetails();
    }, [projectId]);

    const handleSectionChange = (index, value) => {
        const newSections = [...sections];
        newSections[index].title = value;
        setSections(newSections);
    };

    const addSection = () => {
        setSections([...sections, { title: '' }]);
    };

    const removeSection = (index) => {
        const newSections = sections.filter((_, i) => i !== index);
        setSections(newSections);
    };

    const handleSuggestOutline = async () => {
        if (!mainTopic.trim()) {
            setError('Please enter a main topic first.');
            return;
        }
        setIsLoading(true);
        setError('');
        try {
            const response = await api.post(`/projects/${projectId}/suggest-outline`, { main_topic: mainTopic });

            const data = response.data;
            const suggestedSections = data.map(item => ({ title: item.title || item }));
            setSections(suggestedSections);
        } catch (err) {
            console.error(err);
            setError('Failed to suggest an outline.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleGenerateContent = async () => {
        if (!mainTopic.trim()) {
            setError('Please provide a main topic for the document.');
            return;
        }
        const sectionTitles = sections.map(s => s.title.trim()).filter(t => t);
        if (sectionTitles.length === 0) {
            setError('Please add at least one section title.');
            return;
        }
        setIsLoading(true);
        setGeneratedContent([]);
        setError('');
        try {
            const response = await api.post(`/projects/${projectId}/generate`, {
                main_topic: mainTopic,
                section_titles: sectionTitles,
            });
            setGeneratedContent(response.data);
        } catch (err) {
            console.error(err);
            setError('Failed to generate content. Please try again.');
        } finally {
            setIsLoading(false);
        }
    };

    const handleContentUpdate = (sectionId, newContent) => {
        setGeneratedContent(prev =>
            prev.map(section =>
                section.id === sectionId ? { ...section, content: newContent } : section
            )
        );
    };

    const handleExport = async () => {
        setIsExporting(true);
        setError('');

        try {
            const response = await api.get(`/projects/${projectId}/export`, { responseType: 'blob' });

            const file = new Blob([response.data], {
                type: response.headers['content-type']
            });

            const url = window.URL.createObjectURL(file);
            const link = document.createElement('a');
            link.href = url;

            const cd = response.headers['content-disposition'];
            let filename = "document";

            if (cd) {
                const match = cd.match(/filename="?([^"]+)"?/);
                if (match && match[1]) {
                    filename = match[1];
                }
            }

            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);

        } catch (err) {
            console.error(err);
            setError('Failed to export document. Please ensure content was generated.');
        } finally {
            setIsExporting(false);
        }
    };

    return (
        <div className="editor-page-container">
            <div className="editor-header">
                <h1>Document Editor</h1>
                <div className="editor-actions">
                    <button onClick={handleExport} disabled={isExporting} className="editor-button export-button">
                        {isExporting ? 'Exporting...' : 'Export Document'}
                    </button>
                    <Link to="/dashboard" className="editor-button back-button">
                        ← Back to Dashboard
                    </Link>
                </div>
            </div>
            <hr />

            <div className="config-box">
                <h2>1. Configure Document Structure</h2>
                <div>
                    <label>Main Topic / Prompt:</label>
                    <input
                        type="text"
                        value={mainTopic}
                        onChange={(e) => setMainTopic(e.target.value)}
                        placeholder="e.g., The Future of Renewable Energy"
                        className="input-field"
                    />
                </div>

                <button onClick={handleSuggestOutline} disabled={!mainTopic.trim() || isLoading} className="ai-suggest-button">
                    🤖 AI-Suggest Outline
                </button>

                <div>
                    <label>Section Headers:</label>
                    {sections.map((section, index) => (
                        <div key={index} className="section-item">
                            <input
                                type="text"
                                value={section.title}
                                onChange={(e) => handleSectionChange(index, e.target.value)}
                                placeholder={`Section ${index + 1} Title`}
                                className="section-input"
                            />
                            <button onClick={() => removeSection(index)} className="remove-button">
                                Remove
                            </button>
                        </div>
                    ))}
                    <button onClick={addSection} className="add-section-button">+ Add Section</button>
                </div>

                <button onClick={handleGenerateContent} disabled={isLoading} className="generate-button">
                    {isLoading ? 'Generating...' : '✨ Generate Content'}
                </button>

                {error && <p className="error-message">{error}</p>}
            </div>

            {/* THIS IS THE PART THAT DISPLAYS THE EDITOR */}
            {generatedContent.length > 0 && (
                <div style={{ marginTop: '40px' }}>
                    <h2>2. Generated Document (Interactive)</h2>
                    {generatedContent.map((section) => (
                        <SectionEditor
                            key={section.id}
                            section={section}
                            onContentUpdate={handleContentUpdate}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

export default EditorPage;