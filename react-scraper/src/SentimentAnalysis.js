import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function SentimentAnalysis() {
  const [text, setText] = useState('');
  const [data, setData] = useState('');
  const [loading, setLoading] = useState(false);

  const analyzeSentiment = (e) => {
    e.preventDefault();

    if (text.trim() === '') {
      alert('Please enter some text to analyze.');
      return;
    }

    setLoading(true);
    axios.post('/api/scrape', { text: text, postType: 'text' }) // Set postType to 'text' to differentiate this request
      .then(response => {
        setData(response.data); // Update data state with response data
        setLoading(false); // Set loading to false
      })
      .catch(error => {
        console.error('Error analyzing sentiment:', error);
        setLoading(false); // Set loading to false in case of error
      });
  };

  return (
    <div className="SentimentAnalysis">
      <h2>Sentiment Analysis</h2>
      <form onSubmit={analyzeSentiment}>
        <textarea 
          placeholder="Enter text to analyze sentiment" 
          value={text} 
          onChange={(e) => setText(e.target.value)} 
          required 
        />
        <button type="submit" className="App-button">
          Analyze Sentiment
        </button>
      </form>
      <div className="App-result">
        {loading ? 'Analyzing...' : <pre>{data}</pre>}
      </div>
    </div>
  );
}

export default SentimentAnalysis;
