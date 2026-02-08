import React, { useState } from 'react'

function RiskScore({ data }) {
  const [showBreakdown, setShowBreakdown] = useState(false)

  const getScoreColor = (score) => {
    if (score < 40) return 'text-green-600'
    if (score < 70) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score) => {
    if (score < 40) return 'bg-green-100'
    if (score < 70) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  const getDecisionColor = (decision) => {
    if (decision === 'Accept') return 'bg-green-500'
    if (decision === 'Accept with conditions') return 'bg-yellow-500'
    return 'bg-red-500'
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Risk Assessment</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Score Display */}
        <div className={`${getScoreBgColor(data.score)} rounded-lg p-8 text-center`}>
          <p className="text-sm font-medium text-gray-600 uppercase mb-2">Overall Risk Score</p>
          <p className={`text-6xl font-bold ${getScoreColor(data.score)}`}>
            {data.score.toFixed(1)}
          </p>
          <p className="text-sm text-gray-600 mt-2">out of 100</p>
        </div>

        {/* Decision */}
        <div className="flex flex-col justify-between">
          <div>
            <p className="text-sm font-medium text-gray-600 uppercase mb-2">Decision</p>
            <div className={`${getDecisionColor(data.decision)} text-white px-4 py-3 rounded-lg font-semibold text-lg`}>
              {data.decision}
            </div>
            <p className="text-sm text-gray-600 mt-3">
              Confidence: <span className="font-semibold">{data.confidence}</span>
            </p>
            {data.premium_adjustment && (
              <p className="text-sm text-gray-600 mt-1">
                Premium Adjustment: <span className="font-semibold">
                  +{((data.premium_adjustment - 1) * 100).toFixed(1)}%
                </span>
              </p>
            )}
          </div>
        </div>
      </div>

      {/* Confidence Explanation */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-gray-700">{data.confidence_explanation}</p>
      </div>

      {/* Expandable Breakdown */}
      <div className="mt-6">
        <button
          onClick={() => setShowBreakdown(!showBreakdown)}
          className="w-full flex justify-between items-center px-4 py-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          <span className="font-semibold text-gray-800">Risk Calculation Breakdown</span>
          <span className="text-xl">{showBreakdown ? '▼' : '▶'}</span>
        </button>

        {showBreakdown && (
          <div className="mt-4 p-4 bg-gray-50 rounded-lg space-y-3">
            <p className="text-sm text-gray-600 mb-4 font-mono">
              {data.calculation_details}
            </p>
            
            <div className="space-y-2">
              {Object.entries(data.breakdown).map(([category, details]) => (
                <div key={category} className="flex justify-between items-center text-sm">
                  <span className="text-gray-700 capitalize">
                    {category} ({details.weight * 100}%)
                  </span>
                  <span className="font-semibold text-gray-900">
                    {details.score} × {details.weight} = {details.contribution}
                  </span>
                </div>
              ))}
            </div>

            <div className="pt-3 border-t border-gray-300">
              <div className="flex justify-between items-center font-semibold">
                <span>Total Risk Score</span>
                <span className={getScoreColor(data.score)}>{data.score.toFixed(2)}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default RiskScore
