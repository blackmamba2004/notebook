import React, { useEffect, useState } from 'react';
import axios from 'axios';

const NotesList = () => {
    const [notes, setNotes] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchNotes = async () => {
            try {
                const response = await axios.get('/api/v1/notes/');
                setNotes(response.data);
            } catch (err) {
                setError('Error fetching notes');
            }
        };

        fetchNotes();
    }, []);

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h2>Notes</h2>
            <ul>
                {notes.map(note => (
                    <li key={note.id}>
                        <h1>{note.id}</h1>
                        <h3>{note.title}</h3>
                        <p>{note.content}</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default NotesList;
