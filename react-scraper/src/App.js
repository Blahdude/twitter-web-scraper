import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);

  const startScraping = () => {
    setLoading(true);
    axios.get('/api/scrape')
      .then(response => {
        // Assuming the response data is an array of strings or objects
        const resultArray = response.data.data;
        // Join the array with a comma and space
        const formattedData = resultArray.join(', ');
        setData(formattedData);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false);
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        Scrape and Analyze Bitcoin Posts
      </header>
      <main className="App-main">
        <button className="App-button" onClick={startScraping}>
          Start Scraping
        </button>
        <div className="App-result">
          {loading ? 'Scraping...' : data ? <pre>{data}</pre> : 'Click the button to start scraping.'}
        </div>
      </main>
    </div>
  );
}

export default App;
