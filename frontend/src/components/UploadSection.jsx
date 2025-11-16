import React, { useState } from 'react'
import axios from 'axios'

const API_BASE = '/api'

function UploadSection({ onUpload }) {
  const [file, setFile] = useState(null)
  const [source, setSource] = useState('gong')
  const [fileType, setFileType] = useState('csv')
  const [uploading, setUploading] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)
  const [dragActive, setDragActive] = useState(false)

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0])
      setMessage(null)
      setError(null)
    }
  }

  const handleDrag = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0])
      const fileName = e.dataTransfer.files[0].name.toLowerCase()
      if (fileName.endsWith('.csv')) {
        setFileType('csv')
      } else if (fileName.endsWith('.json')) {
        setFileType('json')
      }
      setMessage(null)
      setError(null)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file')
      return
    }

    setUploading(true)
    setMessage(null)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('source', source)

      const endpoint = fileType === 'csv' 
        ? `${API_BASE}/upload/csv`
        : `${API_BASE}/upload/json`

      const response = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 120000, // 2 minutes timeout for large files
      })

      const message = response.data.uploaded 
        ? `Successfully uploaded ${response.data.uploaded} conversation${response.data.uploaded > 1 ? 's' : ''}!${response.data.skipped ? ` (${response.data.skipped} skipped - already exist)` : ''}`
        : 'Upload completed with no new conversations'
      setMessage(message)
      setFile(null)
      if (onUpload) {
        onUpload()
      }
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Upload failed')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="card">
      <h2>Upload Conversation Data</h2>
      
      <div className="input-group">
        <label>Data Source</label>
        <select value={source} onChange={(e) => setSource(e.target.value)}>
          <option value="gong">Gong</option>
          <option value="salesforce">Salesforce</option>
          <option value="planhat">Planhat</option>
          <option value="other">Other</option>
        </select>
      </div>

      <div className="input-group">
        <label>File Type</label>
        <select value={fileType} onChange={(e) => setFileType(e.target.value)}>
          <option value="csv">CSV</option>
          <option value="json">JSON</option>
        </select>
      </div>

      <div className="input-group">
        <label>Select File</label>
        <div
          className={`file-upload-area ${dragActive ? 'dragover' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={() => document.getElementById('file-input').click()}
        >
          <div className="upload-icon">📁</div>
          <p>
            {file ? file.name : 'Click to upload or drag and drop'}
          </p>
          <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.5rem' }}>
            {fileType === 'csv' 
              ? 'CSV should have a "transcript" column'
              : 'JSON should have "transcript" or "text" field'}
          </p>
          <input
            id="file-input"
            type="file"
            className="file-input"
            accept={fileType === 'csv' ? '.csv' : '.json'}
            onChange={handleFileChange}
          />
        </div>
      </div>

      {error && <div className="error">{error}</div>}
      {message && <div className="success">{message}</div>}

      <button
        className="button"
        onClick={handleUpload}
        disabled={!file || uploading}
      >
        {uploading ? 'Uploading...' : 'Upload File'}
      </button>

      <div style={{ marginTop: '2rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px' }}>
        <h3 style={{ marginBottom: '0.5rem' }}>File Format Requirements:</h3>
        <p><strong>CSV:</strong> Must include a "transcript" column. Optional: "conversation_id" and other metadata columns.</p>
        <p style={{ marginTop: '0.5rem' }}>
          <strong>JSON:</strong> Array of objects or single object with "transcript", "text", or "content" field. Optional: "conversation_id" and other metadata.
        </p>
      </div>
    </div>
  )
}

export default UploadSection

