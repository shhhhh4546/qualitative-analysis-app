import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const API_BASE = '/api'

function AggregateInsights() {
  const [source, setSource] = useState('')
  const [loading, setLoading] = useState(false)
  const [insights, setInsights] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchInsights()
  }, [source])

  const fetchInsights = async () => {
    setLoading(true)
    setError(null)

    try {
      const params = source ? { source } : {}
      const response = await axios.get(
        `${API_BASE}/results/aggregate/summary`,
        { params }
      )
      setInsights(response.data)
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to fetch insights')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <div className="loading">Loading insights...</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <div className="error">{error}</div>
      </div>
    )
  }

  if (!insights || insights.total_analyzed === 0) {
    return (
      <div className="card">
        <h2>Aggregate Insights</h2>
        <p>No analysis results available yet. Please upload data and run analysis first.</p>
      </div>
    )
  }

  const painPointsData = insights.pain_points.top.slice(0, 10).map(item => ({
    name: item.point.length > 40 ? item.point.substring(0, 40) + '...' : item.point,
    count: item.count
  }))

  const mediaData = insights.media_consumption.top.slice(0, 10).map(item => ({
    name: item.media,
    count: item.count
  }))

  const compellingData = insights.compelling_points.top.slice(0, 10).map(item => ({
    name: item.point.length > 40 ? item.point.substring(0, 40) + '...' : item.point,
    count: item.count
  }))

  return (
    <div>
      <div className="card">
        <h2>Aggregate Insights</h2>
        
        <div className="input-group" style={{ maxWidth: '300px' }}>
          <label>Filter by Source (Optional)</label>
          <select value={source} onChange={(e) => setSource(e.target.value)}>
            <option value="">All Sources</option>
            <option value="gong">Gong</option>
            <option value="salesforce">Salesforce</option>
            <option value="planhat">Planhat</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div className="insight-item" style={{ marginTop: '1rem' }}>
          <strong>Total Conversations Analyzed:</strong> {insights.total_analyzed}
        </div>
      </div>

      <div className="card">
        <h3>Top Pain Points</h3>
        <p style={{ color: '#666', marginBottom: '1rem' }}>
          Most frequently mentioned problems and challenges
        </p>
        {painPointsData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={painPointsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#667eea" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p>No pain points found</p>
        )}
        
        <div style={{ marginTop: '2rem' }}>
          <h4>All Pain Points:</h4>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {insights.pain_points.top.map((item, idx) => (
              <div key={idx} className="insight-item">
                <strong>{item.point}</strong> <span style={{ color: '#666' }}>({item.count} mentions)</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card">
        <h3>Media Consumption</h3>
        <p style={{ color: '#666', marginBottom: '1rem' }}>
          Media sources and platforms customers mentioned
        </p>
        {mediaData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={mediaData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#764ba2" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p>No media consumption data found</p>
        )}
        
        <div style={{ marginTop: '2rem' }}>
          <h4>All Media Sources:</h4>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {insights.media_consumption.top.map((item, idx) => (
              <div key={idx} className="insight-item">
                <strong>{item.media}</strong> <span style={{ color: '#666' }}>({item.count} mentions)</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card">
        <h3>Compelling Points</h3>
        <p style={{ color: '#666', marginBottom: '1rem' }}>
          Features and benefits that interested customers
        </p>
        {compellingData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={compellingData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="count" fill="#f093fb" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <p>No compelling points found</p>
        )}
        
        <div style={{ marginTop: '2rem' }}>
          <h4>All Compelling Points:</h4>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {insights.compelling_points.top.map((item, idx) => (
              <div key={idx} className="insight-item">
                <strong>{item.point}</strong> <span style={{ color: '#666' }}>({item.count} mentions)</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AggregateInsights

