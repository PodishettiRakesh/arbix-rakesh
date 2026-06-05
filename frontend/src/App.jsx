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

function mapApiErrorsToFields(detail) {
  const fieldErrors = {}

  if (!detail) {
    return { fieldErrors, formError: 'Something went wrong. Please try again.' }
  }

  if (typeof detail === 'string') {
    return { fieldErrors, formError: detail }
  }

  if (Array.isArray(detail)) {
    detail.forEach((item) => {
      const fieldName = item.loc?.[item.loc.length - 1]
      if (fieldName && fieldName !== 'body') {
        fieldErrors[fieldName] = item.msg
      }
    })

    if (Object.keys(fieldErrors).length === 0) {
      return {
        fieldErrors,
        formError: detail.map((item) => item.msg).join(' '),
      }
    }

    return { fieldErrors, formError: null }
  }

  return { fieldErrors, formError: JSON.stringify(detail) }
}

function validateForm(form) {
  const fieldErrors = {}

  if (!form.land_area_acres || Number(form.land_area_acres) <= 0) {
    fieldErrors.land_area_acres = 'Must be greater than 0 acres.'
  }
  if (!form.crop_type.trim()) {
    fieldErrors.crop_type = 'Cannot be empty or whitespace.'
  }
  const repayment = Number(form.repayment_history_score)
  if (form.repayment_history_score === '' || repayment < 0 || repayment > 100) {
    fieldErrors.repayment_history_score = 'Must be between 0 and 100.'
  }

  return fieldErrors
}

function getScoreLevel(score) {
  if (score >= 80) return 'good'
  if (score >= 50) return 'average'
  return 'poor'
}

function FieldError({ message, id }) {
  if (!message) return null
  return (
    <span className="field-error" id={id} role="alert">
      {message}
    </span>
  )
}

export default function App() {
  const [form, setForm] = useState(initialForm)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [fieldErrors, setFieldErrors] = useState({})
  const [formError, setFormError] = useState(null)

  const handleChange = (event) => {
    const { name, value } = event.target
    setForm((previous) => ({ ...previous, [name]: value }))
    setFieldErrors((previous) => {
      if (!previous[name]) return previous
      const next = { ...previous }
      delete next[name]
      return next
    })
    if (formError) {
      setFormError(null)
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault()
    setFieldErrors({})
    setFormError(null)
    setResult(null)

    const clientErrors = validateForm(form)
    if (Object.keys(clientErrors).length > 0) {
      setFieldErrors(clientErrors)
      return
    }

    setLoading(true)

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          land_area_acres: Number(form.land_area_acres),
          crop_type: form.crop_type.trim(),
          repayment_history_score: Number(form.repayment_history_score),
          annual_income_band: form.annual_income_band,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        const { fieldErrors: apiFieldErrors, formError: apiFormError } = mapApiErrorsToFields(
          data.detail,
        )
        setFieldErrors(apiFieldErrors)
        setFormError(apiFormError)
        return
      }

      setResult(data)
    } catch (requestError) {
      setFormError(
        requestError.message ||
          'Could not reach the server. Make sure the backend is running on port 8002.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="page">
      <div className="app">
        <header className="header">
          <p className="eyebrow">Arbix AI Exercise</p>
          <h1>Farmer Credit Scoring</h1>
          <p className="subtitle">
            Enter landholding and repayment details to generate a rule-based credit score.
          </p>
        </header>

        <form className="score-form" onSubmit={handleSubmit} noValidate>
          <div className={`field ${fieldErrors.land_area_acres ? 'has-error' : ''}`}>
            <label htmlFor="land_area_acres">Land Area (acres)</label>
            <input
              id="land_area_acres"
              type="number"
              name="land_area_acres"
              min="0.01"
              step="0.01"
              placeholder="e.g. 3.5"
              value={form.land_area_acres}
              onChange={handleChange}
              aria-invalid={Boolean(fieldErrors.land_area_acres)}
              aria-describedby={fieldErrors.land_area_acres ? 'land_area_acres-error' : undefined}
            />
            <FieldError message={fieldErrors.land_area_acres} id="land_area_acres-error" />
          </div>

          <div className={`field ${fieldErrors.crop_type ? 'has-error' : ''}`}>
            <label htmlFor="crop_type">Crop Type</label>
            <input
              id="crop_type"
              type="text"
              name="crop_type"
              placeholder="e.g. Rice, Wheat, Cotton"
              value={form.crop_type}
              onChange={handleChange}
              aria-invalid={Boolean(fieldErrors.crop_type)}
              aria-describedby={fieldErrors.crop_type ? 'crop_type-error' : undefined}
            />
            <FieldError message={fieldErrors.crop_type} id="crop_type-error" />
          </div>

          <div className={`field ${fieldErrors.repayment_history_score ? 'has-error' : ''}`}>
            <label htmlFor="repayment_history_score">Repayment History Score</label>
            <input
              id="repayment_history_score"
              type="number"
              name="repayment_history_score"
              min="0"
              max="100"
              step="1"
              placeholder="0 to 100"
              value={form.repayment_history_score}
              onChange={handleChange}
              aria-invalid={Boolean(fieldErrors.repayment_history_score)}
              aria-describedby={
                fieldErrors.repayment_history_score ? 'repayment_history_score-error' : undefined
              }
            />
            {!fieldErrors.repayment_history_score && (
              <span className="hint">Score from 0 (poor) to 100 (excellent)</span>
            )}
            <FieldError
              message={fieldErrors.repayment_history_score}
              id="repayment_history_score-error"
            />
          </div>

          <div className={`field ${fieldErrors.annual_income_band ? 'has-error' : ''}`}>
            <label htmlFor="annual_income_band">Annual Income Band</label>
            <select
              id="annual_income_band"
              name="annual_income_band"
              value={form.annual_income_band}
              onChange={handleChange}
              aria-invalid={Boolean(fieldErrors.annual_income_band)}
              aria-describedby={
                fieldErrors.annual_income_band ? 'annual_income_band-error' : undefined
              }
            >
              {INCOME_BANDS.map((band) => (
                <option key={band} value={band}>
                  {band}
                </option>
              ))}
            </select>
            <FieldError message={fieldErrors.annual_income_band} id="annual_income_band-error" />
          </div>

          {formError && (
            <div className="form-error" role="alert">
              <strong>Unable to submit:</strong> {formError}
            </div>
          )}

          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? (
              <>
                <span className="spinner" aria-hidden="true" />
                Submitting...
              </>
            ) : (
              'Get Credit Score'
            )}
          </button>
        </form>

        {result && (
          <div className="result-card">
            <div className="result-header">
              <h2>Scoring Result</h2>
              <span className={`score-badge score-${getScoreLevel(result.score)}`}>
                {getScoreLevel(result.score).toUpperCase()}
              </span>
            </div>

            <div className="score-display">
              <span className="score-label">Credit Score</span>
              <span className="score-value">{result.score}</span>
              <span className="score-range">out of 100</span>
            </div>

            <div className="meta-row">
              <div>
                <span className="meta-label">Request ID</span>
                <span className="meta-value">{result.request_id}</span>
              </div>
              <div>
                <span className="meta-label">Timestamp</span>
                <span className="meta-value">{result.timestamp}</span>
              </div>
            </div>

            <div className="reason-section">
              <h3>Reason Codes</h3>
              <div className="reason-tags">
                {result.reason_codes.map((code) => (
                  <span key={code} className="reason-tag">
                    {code.replaceAll('_', ' ')}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
