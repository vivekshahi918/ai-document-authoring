import React, { useState, useEffect } from 'react'; 
import api from '../services/api';

const SectionEditor = ({ section, onContentUpdate }) => {
    const [refinePrompt, setRefinePrompt] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [comment, setComment] = useState(section.user_notes || section.comment || '');
    const [feedback, setFeedback] = useState(section.feedback || null);

    const [history, setHistory] = useState([]);
    const [showHistory, setShowHistory] = useState(false);

    useEffect(() => {
        setComment(section.user_notes || section.comment || '');
        setFeedback(section.feedback || null);
    }, [section]); 

    useEffect(() => {
        const fetchHistory = async () => {
            try {
                const response = await api.get(`/sections/${section.id}/history`);
                setHistory(response.data);
            } catch (err) {
                console.error("Failed to fetch refinement history", err);
            }
        };

        if (section.id) {
            fetchHistory();
        }
    }, [section.id]); 

    const handleRefine = async () => {
        if (!refinePrompt.trim()) {
            setError('Please enter a refinement instruction.');
            return;
        }

        setIsLoading(true);
        setError('');

        try {
            const response = await api.post(`/sections/${section.id}/refine`, {
                prompt: refinePrompt,
            });

            onContentUpdate(section.id, response.data.content);
            
            const newHistoryEntry = {
                prompt: refinePrompt,
                created_at: new Date().toISOString() 
            };
            setHistory([newHistoryEntry, ...history]);

            setRefinePrompt('');
        } catch (err) {
            setError('Failed to refine content.');
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleFeedback = async (newFeedback) => {
        setFeedback(newFeedback);
        try {
            await api.patch(`/sections/${section.id}`, { feedback: newFeedback });
        } catch (err) {
            console.error("Failed to save feedback");
        }
    };

    const handleCommentChange = (e) => {
        setComment(e.target.value);
    };

    const saveComment = async () => {
        if (comment !== (section.user_notes || section.comment)) {
            try {
                await api.patch(`/sections/${section.id}`, { user_notes: comment });
                console.log("Notes saved!");
            } catch (err) {
                console.error("Failed to save comment");
            }
        }
    };

    return (
        <div style={{ marginBottom: '20px', background: '#282c34', padding: '20px', borderRadius: '8px', border: '1px solid #444' }}>
            <h3>{section.title}</h3>

            <div style={{ whiteSpace: 'pre-wrap', lineHeight: '1.6', background: '#1e1e1e', padding: '15px', borderRadius: '5px', minHeight: '100px' }}>
                {section.content}
            </div>
            
            <div style={{ marginTop: '20px', borderTop: '1px solid #444', paddingTop: '15px' }}>
                <label>Refinement Prompt:</label>
                <input
                    type="text"
                    value={refinePrompt}
                    onChange={(e) => setRefinePrompt(e.target.value)}
                    placeholder="e.g., Make this more formal, summarize in 3 bullet points..."
                    style={{ width: 'calc(100% - 100px)', padding: '8px', marginLeft: '10px' }}
                />
                <button onClick={handleRefine} disabled={isLoading} style={{ width: '80px', padding: '8px', marginLeft: '10px' }}>
                    {isLoading ? '...' : 'Refine'}
                </button>
                {error && <p style={{ color: 'orange', marginTop: '10px' }}>{error}</p>}
            </div>

            <div style={{ marginTop: '20px', borderTop: '1px solid #444', paddingTop: '15px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <div>
                        <label>Your Notes:</label><br />
                        <textarea
                            value={comment}
                            onChange={handleCommentChange}
                            onBlur={saveComment}
                            placeholder="Add private notes for this section..."
                            style={{ width: '400px', height: '60px', marginTop: '5px', background: '#1e1e1e', color: 'white', padding: '8px', borderRadius: '5px', border: '1px solid #555'}}
                        />
                    </div>
                    <div>
                        <label>Content Feedback:</label><br />
                        <button onClick={() => handleFeedback('like')} style={{ background: feedback === 'like' ? 'green' : '#555', padding: '8px 12px', borderRadius: '5px', marginRight: '10px', color: 'white' }}>
                            👍 Like
                        </button>
                        <button onClick={() => handleFeedback('dislike')} style={{ background: feedback === 'dislike' ? 'darkred' : '#555', padding: '8px 12px', borderRadius: '5px', color: 'white' }}>
                            👎 Dislike
                        </button>
                    </div>
                </div>
            </div>

            {/* History Display Section */}
            <div style={{ marginTop: '20px', borderTop: '1px solid #444', paddingTop: '15px' }}>
                <button onClick={() => setShowHistory(!showHistory)} style={{padding: '5px 10px'}}>
                    {showHistory ? 'Hide' : 'Show'} Refinement History ({history.length})
                </button>
                
                {showHistory && (
                    <ul style={{ listStyle: 'none', paddingLeft: '0', marginTop: '10px' }}>
                        {history.length > 0 ? history.map((item, index) => (
                            <li key={index} style={{ background: '#1e1e1e', padding: '8px', borderRadius: '4px', marginBottom: '5px', fontSize: '0.9em' }}>
                                <strong>Prompt:</strong> "{item.prompt}" 
                                <span style={{color: '#999', marginLeft: '10px'}}>({new Date(item.created_at).toLocaleString()})</span>
                            </li>
                        )) : <p style={{color: '#999', marginTop: '10px'}}>No refinement history for this section.</p>}
                    </ul>
                )}
            </div>
        </div>
    );
};

export default SectionEditor;