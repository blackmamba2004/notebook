import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NotesList from './components/NotesList.js';
import NoteDetail from './components/NoteDetail.js';

function App() {
    return (
        <Router>
            <div className="App">
                <Routes>
                    <Route path="/notes/" element={<NotesList />} />
                    <Route path="/notes/:id/" element={<NoteDetail />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;