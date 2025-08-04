import React, { useState } from 'react';
import axios from 'axios';
import './index.css';

export default function CsvToPdf() {
  const [pdfUrl, setPdfUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [fileName, setFileName] = useState('');

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setError('');
    setLoading(true);
    setPdfUrl(null);
    setFileName(file.name);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://127.0.0.1:8000/upload-csv/', formData, {
        responseType: 'blob',
        headers: { 'Content-Type': 'multipart/form-data' }
      });

      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      setPdfUrl(url);
    } catch (err) {
      setError('Upload failed. Please try again.');
    }
    setLoading(false);
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        background: '#17181b',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center'
      }}
    >
      <h2
        style={{
          color: '#fff',
          marginBottom: '1.5rem',
          fontWeight: 400,
          fontSize: '2.4rem',
          letterSpacing: 0.5,
          textAlign: 'center'
        }}
      >
        Welcome to AI-Negotiator
      </h2>
      <label
        htmlFor="csv-upload"
        style={{
          background: '#23242a',
          color: '#fff',
          padding: '0.6rem 1.3rem',
          borderRadius: '7px',
          cursor: 'pointer',
          fontWeight: 500,
          marginBottom: '0.25rem', // Tightened space to file name
          display: 'inline-block',
          fontSize: '1.18rem',
        }}
      >
        Upload file
        <input
          id="csv-upload"
          type="file"
          accept=".csv"
          style={{ display: 'none' }}
          onChange={handleFileChange}
          disabled={loading}
        />
      </label>
      <div style={{
        color: '#aaa',
        marginBottom: '1rem',
        fontSize: '0.95rem',
        textAlign: 'center',
        fontWeight: 400,
        letterSpacing: 0.1
      }}>
        {fileName || 'No file chosen'}
      </div>
      {loading && <div style={{ color: '#bbb', marginTop: '0.6rem' }}>Processing...</div>}
      {error && <div style={{ color: '#e57373', marginTop: '0.6rem' }}>{error}</div>}
      {pdfUrl && (
        <a
          href={pdfUrl}
          download="output.pdf"
          style={{
            marginTop: '1.3rem',
            background: '#448aff',
            color: '#fff',
            padding: '0.7rem 2.0rem',
            borderRadius: '7px',
            textDecoration: 'none',
            fontWeight: 550,
            fontSize: '1.15rem',
            transition: 'background 0.15s'
          }}
        >
          Download PDF
        </a>
      )}
    </div>
  );
}
