import React, { useState } from 'react'

function CategoryCard({ title, score, data, explanation }) {
  const [expanded, setExpanded] = useState(false)

  const getScoreColor = (score) => {
    if (score < 40) return 'bg-green-500'
    if (score < 70) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const getProgressWidth = (score) => `${Math.min(100, score)}%`

  return (
    <div className="bg-white rounded-lg shadow-md p-5 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <h3 className="text-lg font-bold text-gray-800">{title}</h3>
        <span className={`px-3 py-1 rounded-full text-white text-sm font-semibold ${
          score < 40 ? 'bg-green-500' : score < 70 ? 'bg-yellow-500' : 'bg-red-500'
        }`}>
          {score}/100
        </span>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-200 rounded-full h-3 mb-3">
        <div
          className={`h-3 rounded-full ${getScoreColor(score)} transition-all duration-500`}
          style={{ width: getProgressWidth(score) }}
        />
      </div>

      {/* Summary */}
      {explanation && (
        <p className="text-sm text-gray-600 mb-3">{explanation.summary}</p>
      )}

      {/* Expand Button */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="text-brand-red-600 hover:text-brand-red-700 text-sm font-semibold"
      >
        {expanded ? '▼ Show Less' : '▶ Show Details'}
      </button>

      {/* Expanded Content */}
      {expanded && explanation && (
        <div className="mt-4 pt-4 border-t border-gray-200 space-y-3">
          <div>
            <h4 className="font-semibold text-gray-700 mb-2">Key Points:</h4>
            <ul className="list-disc list-inside space-y-1">
              {explanation.details.map((detail, idx) => (
                <li key={idx} className="text-sm text-gray-600">{detail}</li>
              ))}
            </ul>
          </div>

          <div className="p-3 bg-blue-50 rounded">
            <h4 className="font-semibold text-gray-700 mb-1">Recommendation:</h4>
            <p className="text-sm text-gray-700">{explanation.recommendation}</p>
          </div>

          {/* Additional Data */}
          {data && Object.keys(data).length > 0 && (
            <div className="mt-3">
              <h4 className="font-semibold text-gray-700 mb-2">Data Sources:</h4>
              <div className="space-y-1">
                {data.sources && data.sources.map((source, idx) => (
                  <div key={idx} className="text-xs text-gray-500 flex items-center">
                    <span className="mr-2">{'⭐'.repeat(data.reliability || 3)}</span>
                    <span>{source.name}</span>
                  </div>
                ))}
                {data.timestamp && (
                  <p className="text-xs text-gray-400 mt-2">
                    Updated: {new Date(data.timestamp).toLocaleString()}
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

function CategoryBreakdown({ categories }) {
  const categoryTitles = {
    regulatory: 'Regulatory Risk',
    reputation: 'Reputation Risk',
    route: 'Route Risk',
    weather: 'Weather Risk'
  }

  const mainCategories = ['regulatory', 'reputation', 'route', 'weather']

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Risk Category Breakdown</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {mainCategories.map(key => {
          const category = categories[key]
          return (
            <CategoryCard
              key={key}
              title={categoryTitles[key]}
              score={category.score}
              data={category.data}
              explanation={category.explanation}
            />
          )
        })}
      </div>

      {/* Additional Categories */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow-md p-5">
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-lg font-bold text-gray-800">Vessel Risk</h3>
            <span className={`px-3 py-1 rounded-full text-white text-sm font-semibold ${
              categories.vessel.score < 40 ? 'bg-green-500' : 
              categories.vessel.score < 70 ? 'bg-yellow-500' : 'bg-red-500'
            }`}>
              {categories.vessel.score}/100
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 mb-3">
            <div
              className={`h-3 rounded-full ${
                categories.vessel.score < 40 ? 'bg-green-500' : 
                categories.vessel.score < 70 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${Math.min(100, categories.vessel.score)}%` }}
            />
          </div>
          <p className="text-sm text-gray-600">
            {categories.vessel.explanation?.summary}
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-md p-5">
          <div className="flex justify-between items-center mb-3">
            <h3 className="text-lg font-bold text-gray-800">Cargo Risk</h3>
            <span className={`px-3 py-1 rounded-full text-white text-sm font-semibold ${
              categories.cargo.score < 40 ? 'bg-green-500' : 
              categories.cargo.score < 70 ? 'bg-yellow-500' : 'bg-red-500'
            }`}>
              {categories.cargo.score}/100
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 mb-3">
            <div
              className={`h-3 rounded-full ${
                categories.cargo.score < 40 ? 'bg-green-500' : 
                categories.cargo.score < 70 ? 'bg-yellow-500' : 'bg-red-500'
              }`}
              style={{ width: `${Math.min(100, categories.cargo.score)}%` }}
            />
          </div>
          <p className="text-sm text-gray-600">
            {categories.cargo.explanation?.summary}
          </p>
        </div>
      </div>
    </div>
  )
}

export default CategoryBreakdown
