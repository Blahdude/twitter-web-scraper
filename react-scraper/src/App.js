import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import SentimentAnalysis from './SentimentAnalysis'; // Import the new component
import './App.css';

function App() {
  const [data, setData] = useState('');
  const [loading, setLoading] = useState(false);
  const [community, setCommunity] = useState('');
  const [postType, setPostType] = useState('new'); // Default to 'new' posts

  // Function to validate the Reddit community name
  const isValidCommunityName = (name) => {
    // Basic check: non-empty and alphanumeric (Reddit community names can contain underscores as well)
    const regex = /^[a-zA-Z0-9_]+$/;
    return regex.test(name);
  };

  const startScraping = (e) => {
    e.preventDefault(); // Prevent form from reloading the page

    if (!isValidCommunityName(community)) {
      alert('Please enter a valid Reddit community name.');
      return;
    }

    const url = `https://www.reddit.com/r/${community}/${postType}/`;

    setLoading(true);
    console.log("Sending request to /api/scrape with URL:", url);
    axios.post('/api/scrape', { url: url, postType: postType }, { responseType: 'text' })
      .then(response => {
        console.log("Received response:", response.data);
        setData(response.data); // Update data state with response data
        setLoading(false); // Set loading to false
      })
      .catch(error => {
        console.error('Error fetching data:', error);
        setLoading(false); // Set loading to false in case of error
      });
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <nav>
            <Link to="/">Home</Link> | <Link to="/sentiment-analysis">Sentiment Analysis</Link>
          </nav>
          <h1>Scraper</h1>
        </header>
        <main className="App-main">
          <Routes>
            <Route path="/" element={
              <div>
                <form onSubmit={startScraping}>
                  <input 
                    type="text" 
                    placeholder="Enter Reddit community name" 
                    value={community} 
                    onChange={(e) => setCommunity(e.target.value)} 
                    required 
                  />
                  <div>
                    <button 
                      type="button" 
                      className={`App-button ${postType === 'new' ? 'active' : ''}`}
                      onClick={() => setPostType('new')}
                    >
                      New
                    </button>
                    <button 
                      type="button" 
                      className={`App-button ${postType === 'hot' ? 'active' : ''}`}
                      onClick={() => setPostType('hot')}
                    >
                      Hot
                    </button>
                  </div>
                  <button type="submit" className="App-button">
                    Start Scraping
                  </button>
                </form>
                <div className="App-result">
                  {loading ? 'Scraping...' : <pre>{data}</pre>}
                </div>
              </div>
            } />
            <Route path="/sentiment-analysis" element={<SentimentAnalysis />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
