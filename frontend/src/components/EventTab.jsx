import React, { useState } from 'react'

function EventTab({ data }) {
  const [activeTab, setActiveTab] = useState('timeline')

  const tabs = [
    { id: 'timeline', label: 'Timeline' },
    { id: 'categories', label: 'Categories' },
    { id: 'reasoning', label: 'Agent Reasoning' },
    { id: 'evidence', label: 'Evidence' },
    { id: 'trends', label: 'Historical Trends' }
  ]

  return (
    <div className="bg-white rounded-lg shadow-md">
      {/* Tab Navigation */}
      <div className="border-b border-gray-200">
        <div className="flex overflow-x-auto">
          {tabs.map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-4 font-semibold text-sm whitespace-nowrap ${
                activeTab === tab.id
                  ? 'text-brand-red-600 border-b-2 border-brand-red-600'
                  : 'text-gray-600 hover:text-gray-800'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* Tab Content */}
      <div className="p-6">
        {activeTab === 'timeline' && <TimelineView timeline={data.timeline} />}
        {activeTab === 'categories' && <CategoriesView categories={data.categories} />}
        {activeTab === 'reasoning' && <ReasoningView timeline={data.timeline} />}
        {activeTab === 'evidence' && <EvidenceView sources={data.sources} dataQuality={data.data_quality} />}
        {activeTab === 'trends' && <TrendsView historical={data.historical_analysis} />}
      </div>
    </div>
  )
}

function TimelineView({ timeline }) {
  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Event Timeline</h3>
      
      <div className="relative">
        {timeline.map((event, idx) => (
          <div key={idx} className="flex mb-6 relative">
            {/* Timeline line */}
            {idx < timeline.length - 1 && (
              <div className="absolute left-5 top-12 w-0.5 h-full bg-brand-red-300" />
            )}
            
            {/* Timeline dot */}
            <div className="flex-shrink-0 w-10 h-10 rounded-full bg-brand-red-600 flex items-center justify-center text-white font-bold z-10">
              {idx + 1}
            </div>
            
            {/* Event content */}
            <div className="ml-4 flex-1 bg-gray-50 rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-bold text-gray-800">{event.agent}</h4>
                <span className="text-xs text-gray-500">
                  {new Date(event.timestamp).toLocaleTimeString()}
                </span>
              </div>
              
              {event.action && (
                <div className="mb-2">
                  <span className="text-xs font-semibold text-gray-600 uppercase">Action:</span>
                  <p className="text-sm text-gray-700">{event.action}</p>
                </div>
              )}
              
              {event.observation && (
                <div className="mb-2">
                  <span className="text-xs font-semibold text-gray-600 uppercase">Observation:</span>
                  <p className="text-sm text-gray-700">{event.observation}</p>
                </div>
              )}
              
              {event.conclusion && (
                <div className="bg-blue-50 p-2 rounded mt-2">
                  <span className="text-xs font-semibold text-gray-600 uppercase">Conclusion:</span>
                  <p className="text-sm text-gray-700">{event.conclusion}</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

function CategoriesView({ categories }) {
  return (
    <div className="space-y-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Detailed Category Analysis</h3>
      
      {Object.entries(categories).map(([key, category]) => (
        <div key={key} className="border border-gray-200 rounded-lg p-5">
          <div className="flex justify-between items-start mb-3">
            <h4 className="text-lg font-bold text-gray-800 capitalize">{key} Risk</h4>
            <span className={`px-3 py-1 rounded-full text-white text-sm font-semibold ${
              category.score < 40 ? 'bg-green-500' : 
              category.score < 70 ? 'bg-yellow-500' : 'bg-red-500'
            }`}>
              {category.score}/100
            </span>
          </div>

          {category.explanation && (
            <>
              <p className="text-sm text-gray-700 mb-3">{category.explanation.summary}</p>
              
              {category.explanation.details && (
                <div className="bg-gray-50 p-3 rounded mb-3">
                  <h5 className="font-semibold text-sm text-gray-700 mb-2">Details:</h5>
                  <ul className="list-disc list-inside space-y-1">
                    {category.explanation.details.map((detail, idx) => (
                      <li key={idx} className="text-sm text-gray-600">{detail}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {category.explanation.recommendation && (
                <div className="bg-blue-50 p-3 rounded">
                  <h5 className="font-semibold text-sm text-gray-700 mb-1">Recommendation:</h5>
                  <p className="text-sm text-gray-700">{category.explanation.recommendation}</p>
                </div>
              )}
            </>
          )}
        </div>
      ))}
    </div>
  )
}

function ReasoningView({ timeline }) {
  return (
    <div className="space-y-4">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Complete AI Reasoning (ReAct Pattern)</h3>
      <p className="text-sm text-gray-600 mb-6">
        This shows the complete thought process of each AI agent using the Thought → Action → Observation → Conclusion pattern.
      </p>
      
      {timeline.map((event, idx) => (
        <div key={idx} className="border border-gray-200 rounded-lg p-5">
          <div className="flex items-start mb-4">
            <div className="flex-shrink-0 w-8 h-8 rounded-full bg-brand-red-600 flex items-center justify-center text-white font-bold text-sm">
              {idx + 1}
            </div>
            <div className="ml-3 flex-1">
              <h4 className="font-bold text-gray-800">{event.agent}</h4>
              <span className="text-xs text-gray-500">{new Date(event.timestamp).toLocaleTimeString()}</span>
            </div>
          </div>

          <div className="space-y-3 ml-11">
            {event.thought && (
              <div className="bg-purple-50 p-3 rounded">
                <span className="text-xs font-semibold text-purple-700 uppercase">💭 Thought:</span>
                <p className="text-sm text-gray-700 mt-1">{event.thought}</p>
              </div>
            )}

            {event.action && (
              <div className="bg-blue-50 p-3 rounded">
                <span className="text-xs font-semibold text-blue-700 uppercase">⚡ Action:</span>
                <p className="text-sm text-gray-700 mt-1">{event.action}</p>
              </div>
            )}

            {event.observation && (
              <div className="bg-yellow-50 p-3 rounded">
                <span className="text-xs font-semibold text-yellow-700 uppercase">👁️ Observation:</span>
                <p className="text-sm text-gray-700 mt-1">{event.observation}</p>
              </div>
            )}

            {event.conclusion && (
              <div className="bg-green-50 p-3 rounded">
                <span className="text-xs font-semibold text-green-700 uppercase">✅ Conclusion:</span>
                <p className="text-sm text-gray-700 mt-1">{event.conclusion}</p>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  )
}

function EvidenceView({ sources, dataQuality }) {
  return (
    <div className="space-y-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Data Sources & Evidence</h3>
      
      {/* Data Quality Summary */}
      <div className="bg-gradient-to-r from-blue-50 to-transparent border-l-4 border-blue-500 p-4 rounded">
        <h4 className="font-bold text-gray-800 mb-2">Data Quality Assessment</h4>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <p className="text-xs text-gray-600">Overall Score</p>
            <p className="text-2xl font-bold text-blue-700">{(dataQuality.score * 100).toFixed(0)}%</p>
          </div>
          <div>
            <p className="text-xs text-gray-600">Sources</p>
            <p className="text-2xl font-bold text-blue-700">{dataQuality.sources_count}</p>
          </div>
          <div>
            <p className="text-xs text-gray-600">Cross-Reference</p>
            <p className="text-2xl font-bold text-blue-700">
              {dataQuality.cross_reference_valid ? '✓' : '✗'}
            </p>
          </div>
        </div>
      </div>

      {/* Sources List */}
      <div>
        <h4 className="font-bold text-gray-800 mb-3">Verified Data Sources</h4>
        
        {sources && sources.length > 0 ? (
          <div className="space-y-3">
            {sources.map((source, idx) => (
              <div key={idx} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <h5 className="font-semibold text-gray-800">{source.name}</h5>
                  <div className="flex items-center">
                    <span className="text-yellow-500 mr-1">{'⭐'.repeat(source.reliability || 3)}</span>
                    <span className="text-xs text-gray-500">({source.reliability || 3}/5)</span>
                  </div>
                </div>
                
                {source.url && (
                  <a href={source.url} target="_blank" rel="noopener noreferrer" 
                     className="text-xs text-brand-red-600 hover:underline">
                    {source.url}
                  </a>
                )}
                
                {source.checksum && (
                  <p className="text-xs text-gray-400 mt-2 font-mono">
                    Checksum: {source.checksum.substring(0, 16)}...
                  </p>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p className="text-sm text-gray-600">No external sources verified for this analysis.</p>
        )}
      </div>
    </div>
  )
}

function TrendsView({ historical }) {
  return (
    <div className="space-y-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">Historical Trends Analysis</h3>
      
      {/* Statistics Summary */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="bg-blue-50 rounded-lg p-4 text-center">
          <p className="text-xs text-gray-600 uppercase mb-1">Total Applications</p>
          <p className="text-3xl font-bold text-blue-700">{historical.total_applications}</p>
        </div>
        
        <div className="bg-green-50 rounded-lg p-4 text-center">
          <p className="text-xs text-gray-600 uppercase mb-1">Similar Found</p>
          <p className="text-3xl font-bold text-green-700">{historical.similar_applications}</p>
        </div>
        
        <div className="bg-yellow-50 rounded-lg p-4 text-center">
          <p className="text-xs text-gray-600 uppercase mb-1">Acceptance Rate</p>
          <p className="text-3xl font-bold text-yellow-700">
            {(historical.statistics.acceptance_rate * 100).toFixed(0)}%
          </p>
        </div>
        
        <div className="bg-red-50 rounded-lg p-4 text-center">
          <p className="text-xs text-gray-600 uppercase mb-1">Avg Risk Score</p>
          <p className="text-3xl font-bold text-red-700">
            {historical.statistics.average_risk_score.toFixed(1)}
          </p>
        </div>
      </div>

      {/* Decision Distribution */}
      <div className="bg-white border border-gray-200 rounded-lg p-5">
        <h4 className="font-bold text-gray-800 mb-3">Decision Distribution</h4>
        <div className="space-y-2">
          {Object.entries(historical.statistics.decision_distribution).map(([decision, count]) => {
            const percentage = (count / historical.similar_applications * 100).toFixed(1)
            return (
              <div key={decision}>
                <div className="flex justify-between text-sm mb-1">
                  <span className="text-gray-700">{decision}</span>
                  <span className="font-semibold">{count} ({percentage}%)</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-brand-red-600 h-2 rounded-full transition-all"
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Top Similar Applications */}
      <div>
        <h4 className="font-bold text-gray-800 mb-3">Top Similar Applications</h4>
        <div className="space-y-3">
          {historical.top_matches.slice(0, 5).map((app, idx) => (
            <div key={idx} className="border border-gray-200 rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h5 className="font-semibold text-gray-800">{app.vessel_name}</h5>
                  <p className="text-xs text-gray-500">{app.owner}</p>
                </div>
                <span className={`px-2 py-1 rounded text-xs font-semibold ${
                  app.decision === 'Accept' ? 'bg-green-100 text-green-800' :
                  app.decision === 'Accept with conditions' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {app.decision}
                </span>
              </div>
              
              <div className="grid grid-cols-3 gap-2 text-xs text-gray-600">
                <div>
                  <span className="font-semibold">Route:</span> {app.departure_port} → {app.destination_port}
                </div>
                <div>
                  <span className="font-semibold">Cargo:</span> {app.cargo_type}
                </div>
                <div>
                  <span className="font-semibold">Risk:</span> {app.risk_score}
                </div>
              </div>
              
              <div className="mt-2 flex justify-between items-center">
                <span className="text-xs text-gray-500">
                  {new Date(app.date).toLocaleDateString()}
                </span>
                <span className="text-xs font-semibold text-brand-red-600">
                  Similarity: {app.similarity_score}%
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default EventTab
