import React, { useState } from 'react'
import axios from 'axios'

const API_BASE = '/api'

function AnalysisDashboard() {
  const [source, setSource] = useState('')
  const [limit, setLimit] = useState(100)
  const [analyzing, setAnalyzing] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)
  const [results, setResults] = useState(null)

  const handleAnalyze = async () => {
    setAnalyzing(true)
    setMessage(null)
    setError(null)
    setResults(null)

    try {
      const params = { limit }
      if (source) {
        params.source = source
      }

      const response = await axios.post(
        `${API_BASE}/analysis/analyze-batch`,
        null,
        { params }
      )

      setResults(response.data)
      setMessage(
        `Analysis complete! Analyzed ${response.data.analyzed} conversations.`
      )
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Analysis failed')
    } finally {
      setAnalyzing(false)
    }
  }

  return (
    <div>
      <div className="card">
        <h2>Run Analysis</h2>
        
        <div className="input-group">
          <label>Data Source (Optional - leave empty for all sources)</label>
          <select value={source} onChange={(e) => setSource(e.target.value)}>
            <option value="">All Sources</option>
            <option value="gong">Gong</option>
            <option value="salesforce">Salesforce</option>
            <option value="planhat">Planhat</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="input-group">
          <label>Number of Conversations to Analyze</label>
          <input
            type="number"
            value={limit}
            onChange={(e) => setLimit(parseInt(e.target.value) || 100)}
            min="1"
            max="1000"
          />
        </div>

        {error && <div className="error">{error}</div>}
        {message && <div className="success">{message}</div>}

        <button
          className="button"
          onClick={handleAnalyze}
          disabled={analyzing}
        >
          {analyzing ? 'Analyzing...' : 'Start Analysis'}
        </button>

        {results && (
          <div style={{ marginTop: '2rem' }}>
            <h3>Analysis Results</h3>
            <div className="grid">
              <div className="insight-item">
                <strong>Analyzed:</strong> {results.analyzed}
              </div>
              <div className="insight-item">
                <strong>Already Analyzed:</strong> {results.already_analyzed}
              </div>
              {results.errors && results.errors.length > 0 && (
                <div className="insight-item">
                  <strong>Errors:</strong> {results.errors.length}
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      <div className="card">
        <h2>Analysis Process</h2>
        <p>
          The analysis uses AI to extract:
        </p>
        <ul style={{ marginTop: '1rem', lineHeight: '1.8' }}>
          <li><strong>Pain Points:</strong> Problems, challenges, and frustrations mentioned by customers</li>
          <li><strong>Media Consumption:</strong> Podcasts, blogs, social media, and other media sources customers follow</li>
          <li><strong>Compelling Points:</strong> Features, benefits, or aspects that interested or excited customers</li>
        </ul>
        <p style={{ marginTop: '1rem', color: '#666' }}>
          Note: Analysis may take several minutes for large batches. The system will skip conversations that have already been analyzed.
        </p>
      </div>
    </div>
  )
}

export default AnalysisDashboard

