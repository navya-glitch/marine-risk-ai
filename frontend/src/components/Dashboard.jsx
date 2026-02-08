import React, { useState } from 'react'
import axios from 'axios'
import InputForm from './InputForm'
import RiskScore from './RiskScore'
import CategoryBreakdown from './CategoryBreakdown'
import Charts from './Charts'
import Recommendations from './Recommendations'
import EventTab from './EventTab'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function Dashboard() {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleAnalyze = async (formData) => {
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/api/analyze`, formData)
      setResult(response.data.data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-brand-red-600 text-white py-6 shadow-lg">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold">🚢 Agentic AI - 360° External Risk Insight</h1>
          <p className="text-brand-red-100 mt-1">Ocean Marine Insurance Underwriting in &lt;60 seconds</p>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Input Form */}
        <InputForm 
          onSubmit={handleAnalyze} 
          loading={loading} 
          entities={result?.entities}
        />

        {/* Loading State */}
        {loading && (
          <div className="mt-8 bg-white rounded-lg shadow-lg p-8 text-center">
            <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-brand-red-600 mx-auto"></div>
            <p className="mt-4 text-gray-600 text-lg">Analyzing risk factors... Please wait</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="mt-8 bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <p className="text-red-700">{error}</p>
          </div>
        )}

        {/* Results */}
        {result && !loading && (
          <div className="space-y-6 mt-8">
            {/* Risk Score Card */}
            <RiskScore data={result.overall_risk} />

            {/* Category Breakdown */}
            <CategoryBreakdown categories={result.categories} />

            {/* Charts */}
            <Charts data={result} />

            {/* Recommendations */}
            <Recommendations data={result.recommendations} />

            {/* Event Tab */}
            <EventTab data={result} />
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard
