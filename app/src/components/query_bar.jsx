import React, { useState } from 'react';
import { useContext } from 'react';

const QueryBar = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState(''); 

    const handleQueryChange = (event) => {
        setQuery(event.target.value);
    };

    const handleQuerySubmit = () => {
        fetch(`http://127.0.0.1:8000/api/tree/?text=${query}`)
            .then(response => response.json())
            .then(data => setResults(data))
            .then(console.log(JSON.parse(results)))

    };

    return (
        <div>
            <input type="text" value={query} onChange={handleQueryChange} />
            <button onClick={handleQuerySubmit}>Submit</button>
        </div>
    );
};

export default QueryBar;