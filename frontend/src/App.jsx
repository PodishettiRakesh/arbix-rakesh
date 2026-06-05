import { useState } from 'react'
import './App.css'

const API_URL = 'http://localhost:8002/score'

const INCOME_BANDS = ['<2L', '2-5L', '5-10L', '>10L']

const initialForm = {
  land_area_acres: '',
  crop_type: '',
  repayment_history_score: '',
  annual_income_band: '<2L',
}

function formatError(detail) {
  if (!detail) {
    return 'Request failed'
  }
  if (typeof detail === 'string') {
    return detail
  }
  if (Array.isArray(detail)) {
    return detail.map((item) => `${item.loc?.slice(1).join('.')}: ${item.msg}`).join('; ')
  }
  return JSON.stringify(detail)
}

export default function App() {
  const [form, setForm] = useState(initialForm)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((previous) => ({ ...previous, [name]: value }))
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          land_area_acres: Number(form.land_area_acres),
          crop_type: form.crop_type,
          repayment_history_score: Number(form.repayment_history_score),
          annual_income_band: form.annual_income_band,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        setError(formatError(data.detail))
        return
      }

      setResult(data)
    } catch (requestError) {
      setError(requestError.message || 'Network error. Is the backend running on port 8002?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <h1>Farmer Credit Scoring</h1>
      <p className="subtitle">Submit land and repayment details to get a credit score.</p>

      <form className="score-form" onSubmit={handleSubmit}>
        <label>
          Land Area (acres)
          <input
            type="number"
            name="land_area_acres"
            min="0.01"
            step="0.01"
            value={form.land_area_acres}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Crop Type
          <input
            type="text"
            name="crop_type"
            value={form.crop_type}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Repayment History Score (0-100)
          <input
            type="number"
            name="repayment_history_score"
            min="0"
            max="100"
            step="1"
            value={form.repayment_history_score}
            onChange={handleChange}
            required
          />
        </label>

        <label>
          Annual Income Band
          <select
            name="annual_income_band"
            value={form.annual_income_band}
            onChange={handleChange}
          >
            {INCOME_BANDS.map((band) => (
              <option key={band} value={band}>
                {band}
              </option>
            ))}
          </select>
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Submitting...' : 'Get Score'}
        </button>
      </form>

      {loading && <p className="status">Submitting...</p>}

      {error && (
        <div className="error" role="alert">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="result">
          <p className="score">Score: {result.score}</p>
          <h2>Reason Codes:</h2>
          <ul>
            {result.reason_codes.map((code) => (
              <li key={code}>{code}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
