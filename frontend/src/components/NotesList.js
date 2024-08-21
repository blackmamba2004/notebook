import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const NotesList = () => {
    const [notes, setNotes] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchNotes = async () => {
            try {
                const response = await axios.get('/notes/');
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
                        <Link to={`/notes/${note.id}/`}>
                            <h3>{note.title}</h3>
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default NotesList;