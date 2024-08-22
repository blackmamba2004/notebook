import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const NotesList = () => {
    const [notes, setNotes] = useState([]);
    const [nextPage, setNextPage] = useState(null);
    const [previousPage, setPreviousPage] = useState(null);
    const [error, setError] = useState(null);
    const [currentPageUrl, setCurrentPageUrl] = useState('/notes/');

    useEffect(() => {
        const fetchNotes = async () => {
            try {
                const response = await axios.get(currentPageUrl);
                setNotes(response.data.results);
                setNextPage(response.data.next);
                setPreviousPage(response.data.previous);
            } catch (err) {
                setError('Error fetching notes');
            }
        };

        fetchNotes();
    }, [currentPageUrl]);

    const handleNextPage = () => {
        if (nextPage) {
            setCurrentPageUrl(nextPage);
        }
    };

    const handlePreviousPage = () => {
        if (previousPage) {
            setCurrentPageUrl(previousPage);
        }
    };

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
            <div>
                <button onClick={handlePreviousPage} disabled={!previousPage}>
                    Previous
                </button>
                <button onClick={handleNextPage} disabled={!nextPage}>
                    Next
                </button>
            </div>
        </div>
    );
};

export default NotesList;