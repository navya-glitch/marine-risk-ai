import React from 'react'
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'

function Charts({ data }) {
  // Prepare radar chart data
  const radarData = [
    { category: 'Regulatory', value: data.categories.regulatory.score },
    { category: 'Reputation', value: data.categories.reputation.score },
    { category: 'Route', value: data.categories.route.score },
    { category: 'Weather', value: data.categories.weather.score },
    { category: 'Vessel', value: data.categories.vessel.score },
    { category: 'Cargo', value: data.categories.cargo.score },
  ]

  // Prepare bar chart data (historical comparison)
  const barData = data.historical_analysis.top_matches.slice(0, 5).map((app, idx) => ({
    name: `App ${idx + 1}`,
    risk: app.risk_score,
    current: idx === 0 ? data.overall_risk.score : null
  }))

  // Add current application
  barData.unshift({
    name: 'Current',
    risk: data.overall_risk.score,
    current: data.overall_risk.score
  })

  // Prepare pie chart data
  const pieData = Object.entries(data.overall_risk.breakdown).map(([key, value]) => ({
    name: key.charAt(0).toUpperCase() + key.slice(1),
    value: value.contribution
  }))

  const COLORS = ['#DC2626', '#EF4444', '#F87171', '#FCA5A5', '#FECACA', '#FEE2E2']

  return (
    <div>
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Risk Analysis Charts</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Radar Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Multi-Dimensional Risk View</h3>
          <ResponsiveContainer width="100%" height={300}>
            <RadarChart data={radarData}>
              <PolarGrid stroke="#e5e7eb" />
              <PolarAngleAxis dataKey="category" tick={{ fill: '#6b7280', fontSize: 12 }} />
              <PolarRadiusAxis angle={90} domain={[0, 100]} tick={{ fill: '#6b7280' }} />
              <Radar name="Risk Score" dataKey="value" stroke="#DC2626" fill="#DC2626" fillOpacity={0.6} />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        {/* Bar Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Historical Comparison</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
              <XAxis dataKey="name" tick={{ fill: '#6b7280', fontSize: 12 }} />
              <YAxis domain={[0, 100]} tick={{ fill: '#6b7280' }} />
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
              <Bar dataKey="risk" fill="#DC2626" />
              <Bar dataKey="current" fill="#10B981" />
            </BarChart>
          </ResponsiveContainer>
          <p className="text-xs text-gray-500 mt-2 text-center">
            Comparing with {data.historical_analysis.similar_applications} similar applications
          </p>
        </div>

        {/* Pie Chart */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">Risk Contribution Breakdown</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {pieData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#fff', border: '1px solid #e5e7eb', borderRadius: '8px' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  )
}

export default Charts
