import React, { useState } from 'react'

const COUNTRIES = [
  'Panama', 'Liberia', 'Marshall Islands', 'Hong Kong', 'Singapore', 
  'Malta', 'Bahamas', 'Cyprus', 'Greece', 'China'
]

const CARGO_TYPES = ['Container', 'Bulk', 'Tanker', 'Reefer', 'RoRo']

function InputForm({ onSubmit, loading, entities }) {
  const [formData, setFormData] = useState({
    vessel_name: '',
    imo_number: '',
    owner: '',
    country_of_registry: 'Panama',
    departure_port: '',
    destination_port: '',
    cargo_type: 'Container'
  })

  const [errors, setErrors] = useState({})

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
    // Clear error for this field
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }))
    }
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.vessel_name.trim()) {
      newErrors.vessel_name = 'Vessel name is required'
    }
    
    if (!formData.imo_number.trim()) {
      newErrors.imo_number = 'IMO number is required'
    } else if (!/^IMO\d{7}$/.test(formData.imo_number)) {
      newErrors.imo_number = 'IMO format should be IMO followed by 7 digits'
    }
    
    if (!formData.owner.trim()) {
      newErrors.owner = 'Owner company is required'
    }
    
    if (!formData.departure_port.trim()) {
      newErrors.departure_port = 'Departure port is required'
    }
    
    if (!formData.destination_port.trim()) {
      newErrors.destination_port = 'Destination port is required'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    if (validateForm()) {
      onSubmit(formData)
    }
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">Vessel Information</h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Vessel Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Vessel Name *
            </label>
            <input
              type="text"
              name="vessel_name"
              value={formData.vessel_name}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-brand-red-500 ${
                errors.vessel_name ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="e.g., MV Neptune Star"
              disabled={loading}
            />
            {errors.vessel_name && (
              <p className="text-red-500 text-xs mt-1">{errors.vessel_name}</p>
            )}
          </div>

          {/* IMO Number */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              IMO Number *
            </label>
            <input
              type="text"
              name="imo_number"
              value={formData.imo_number}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-brand-red-500 ${
                errors.imo_number ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="e.g., IMO9547821"
              disabled={loading}
            />
            {errors.imo_number && (
              <p className="text-red-500 text-xs mt-1">{errors.imo_number}</p>
            )}
          </div>

          {/* Owner Company */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Owner Company *
            </label>
            <input
              type="text"
              name="owner"
              value={formData.owner}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-brand-red-500 ${
                errors.owner ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="e.g., Neptune Maritime Corp"
              disabled={loading}
            />
            {errors.owner && (
              <p className="text-red-500 text-xs mt-1">{errors.owner}</p>
            )}
          </div>

          {/* Country of Registry */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Country of Registry *
            </label>
            <select
              name="country_of_registry"
              value={formData.country_of_registry}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-red-500"
              disabled={loading}
            >
              {COUNTRIES.map(country => (
                <option key={country} value={country}>{country}</option>
              ))}
            </select>
          </div>

          {/* Departure Port */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Departure Port *
            </label>
            <input
              type="text"
              name="departure_port"
              value={formData.departure_port}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-brand-red-500 ${
                errors.departure_port ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="e.g., Rotterdam"
              disabled={loading}
            />
            {errors.departure_port && (
              <p className="text-red-500 text-xs mt-1">{errors.departure_port}</p>
            )}
          </div>

          {/* Destination Port */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Destination Port *
            </label>
            <input
              type="text"
              name="destination_port"
              value={formData.destination_port}
              onChange={handleChange}
              className={`w-full px-3 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-brand-red-500 ${
                errors.destination_port ? 'border-red-500' : 'border-gray-300'
              }`}
              placeholder="e.g., Shanghai"
              disabled={loading}
            />
            {errors.destination_port && (
              <p className="text-red-500 text-xs mt-1">{errors.destination_port}</p>
            )}
          </div>

          {/* Cargo Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Cargo Type *
            </label>
            <select
              name="cargo_type"
              value={formData.cargo_type}
              onChange={handleChange}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-brand-red-500"
              disabled={loading}
            >
              {CARGO_TYPES.map(type => (
                <option key={type} value={type}>{type}</option>
              ))}
            </select>
          </div>
        </div>

        {/* Submit Button */}
        <div className="flex justify-end mt-6">
          <button
            type="submit"
            disabled={loading}
            className="px-8 py-3 bg-brand-red-600 text-white font-semibold rounded-md hover:bg-brand-red-700 focus:outline-none focus:ring-2 focus:ring-brand-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Analyzing...' : '🔍 Analyze Risk'}
          </button>
        </div>
      </form>

      {/* Entity Recognition Badges */}
      {entities && (
        <div className="mt-6 pt-6 border-t border-gray-200">
          <h3 className="text-lg font-semibold text-gray-800 mb-3">Entity Recognition Results</h3>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
            {Object.entries(entities).map(([key, entity]) => (
              <div key={key} className="bg-gray-50 rounded-md p-3">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <p className="text-xs text-gray-500 uppercase">{entity.type}</p>
                    <p className="text-sm font-medium text-gray-900 mt-1 break-all">
                      {typeof entity.value === 'string' ? entity.value : JSON.stringify(entity.value)}
                    </p>
                  </div>
                  <span className={`ml-2 px-2 py-1 text-xs font-semibold rounded ${
                    entity.confidence >= 0.9 ? 'bg-green-100 text-green-800' :
                    entity.confidence >= 0.7 ? 'bg-yellow-100 text-yellow-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    {(entity.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default InputForm
