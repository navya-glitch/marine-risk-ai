import React from 'react'

function Recommendations({ data }) {
  const getDecisionColor = (decision) => {
    if (decision === 'Accept') return 'bg-green-500'
    if (decision.includes('conditions')) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const getPriorityColor = (priority) => {
    if (priority === 'HIGH') return 'bg-red-100 text-red-800'
    if (priority === 'MEDIUM') return 'bg-yellow-100 text-yellow-800'
    return 'bg-green-100 text-green-800'
  }

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">AI Recommendations</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Primary Decision */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Primary Decision</h3>
          
          <div className={`${getDecisionColor(data.primary_decision.decision)} text-white px-4 py-3 rounded-lg mb-4`}>
            <p className="font-bold text-xl">{data.primary_decision.decision}</p>
            <p className="text-sm mt-1">Confidence: {data.primary_decision.confidence}</p>
          </div>

          <div className="bg-blue-50 p-4 rounded-lg">
            <p className="text-sm text-gray-700">{data.primary_decision.reasoning}</p>
          </div>
        </div>

        {/* Historical Context */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Historical Context</h3>
          
          <div className="space-y-3">
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
              <span className="text-sm text-gray-600">Similar Applications</span>
              <span className="font-bold text-gray-900">{data.historical_context.similar_applications}</span>
            </div>
            
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
              <span className="text-sm text-gray-600">Average Premium</span>
              <span className="font-bold text-gray-900">{data.historical_context.average_premium}</span>
            </div>
            
            <div className="flex justify-between items-center p-3 bg-gray-50 rounded">
              <span className="text-sm text-gray-600">Acceptance Rate</span>
              <span className="font-bold text-gray-900">{data.historical_context.acceptance_rate}</span>
            </div>
          </div>

          <div className="mt-4 p-3 bg-blue-50 rounded">
            <p className="text-sm text-gray-700">{data.historical_context.insight}</p>
          </div>
        </div>

        {/* Required Conditions */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Required Conditions</h3>
          
          <div className="space-y-3">
            {data.required_conditions.map((condition, idx) => (
              <div key={idx} className="border-l-4 border-brand-red-600 pl-4 py-2">
                <div className="flex justify-between items-start mb-2">
                  <p className="font-semibold text-gray-800">{condition.condition}</p>
                  <span className={`px-2 py-1 rounded text-xs font-semibold ${getPriorityColor(condition.priority)}`}>
                    {condition.priority}
                  </span>
                </div>
                <p className="text-sm text-gray-600">{condition.reasoning}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Risk Mitigation Options */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Risk Mitigation Options</h3>
          
          {data.risk_mitigation.length > 0 ? (
            <div className="space-y-4">
              {data.risk_mitigation.map((option, idx) => (
                <div key={idx} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex justify-between items-start mb-2">
                    <h4 className="font-semibold text-gray-800">{option.category}</h4>
                    <span className="text-xs text-gray-500">{option.cost} cost</span>
                  </div>
                  <p className="text-sm text-gray-700 mb-2">{option.option}</p>
                  <p className="text-xs text-green-700 bg-green-50 px-2 py-1 rounded">
                    {option.impact}
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-sm text-gray-600">No specific mitigation options required for this low-risk profile.</p>
          )}
        </div>
      </div>

      {/* Business Insights */}
      <div className="mt-6 bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-bold text-gray-800 mb-4">Business Insights</h3>
        
        <div className="space-y-3">
          {data.business_insights.map((insight, idx) => (
            <div key={idx} className="flex items-start p-3 bg-gradient-to-r from-blue-50 to-transparent rounded-lg">
              <span className="text-2xl mr-3">{insight.split(' ')[0]}</span>
              <p className="text-sm text-gray-700 flex-1">{insight.split(' ').slice(1).join(' ')}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default Recommendations
