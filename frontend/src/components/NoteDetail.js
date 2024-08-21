import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const NoteDetail = () => {
    const { id } = useParams();
    const [note, setNote] = useState(null);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchNote = async () => {
            try {
                const response = await axios.get(`/notes/${id}/`);
                setNote(response.data);
            } catch (err) {
                setError('Error fetching note');
            }
        };

        fetchNote();
    }, [id]);

    if (error) {
        return <div>{error}</div>;
    }

    if (!note) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h2>{note.title}</h2>
            <p>{note.content}</p>
        </div>
    );
};

export default NoteDetail;