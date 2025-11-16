import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'
import UploadSection from './components/UploadSection'
import AnalysisDashboard from './components/AnalysisDashboard'
import AggregateInsights from './components/AggregateInsights'

const API_BASE = '/api'

function App() {
  const [activeTab, setActiveTab] = useState('upload')
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API_BASE}/upload/stats`)
      setStats(response.data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>📊 Qualitative Data Analysis</h1>
        <p>Analyze customer conversations to extract pain points, media consumption, and compelling points</p>
        {stats && (
          <div className="stats-banner">
            <span>Total Conversations: <strong>{stats.total_conversations}</strong></span>
            {Object.entries(stats.by_source).map(([source, count]) => (
              <span key={source}>{source}: <strong>{count}</strong></span>
            ))}
          </div>
        )}
      </header>

      <nav className="tab-nav">
        <button
          className={activeTab === 'upload' ? 'active' : ''}
          onClick={() => setActiveTab('upload')}
        >
          📤 Upload Data
        </button>
        <button
          className={activeTab === 'analyze' ? 'active' : ''}
          onClick={() => setActiveTab('analyze')}
        >
          🔍 Analyze
        </button>
        <button
          className={activeTab === 'insights' ? 'active' : ''}
          onClick={() => setActiveTab('insights')}
        >
          📈 Insights
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'upload' && (
          <UploadSection onUpload={fetchStats} />
        )}
        {activeTab === 'analyze' && (
          <AnalysisDashboard />
        )}
        {activeTab === 'insights' && (
          <AggregateInsights />
        )}
      </main>
    </div>
  )
}

export default App

