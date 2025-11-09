import { useState, useEffect } from 'react'

function SystemControls() {
  const [systemStatus, setSystemStatus] = useState({
    sentry_running: false,
    sentry_available: false,
    loading: true
  })
  const [actionLoading, setActionLoading] = useState(false)

  const API_URL = 'http://localhost:5000'

  // Fetch system status on mount and periodically
  useEffect(() => {
    fetchStatus()
    const interval = setInterval(fetchStatus, 2000) // Update every 2 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchStatus = async () => {
    try {
      const response = await fetch(`${API_URL}/system/status`)
      const data = await response.json()
      setSystemStatus({
        sentry_running: data.sentry_running,
        sentry_available: data.sentry_available,
        loading: false
      })
    } catch (error) {
      console.error('Failed to fetch system status:', error)
      setSystemStatus(prev => ({ ...prev, loading: false }))
    }
  }

  const handleToggle = async () => {
    setActionLoading(true)
    try {
      const endpoint = systemStatus.sentry_running ? '/system/stop' : '/system/start'
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
      })
      const data = await response.json()
      console.log('Toggle response:', data)
      await fetchStatus()
    } catch (error) {
      console.error('Failed to toggle system:', error)
    } finally {
      setActionLoading(false)
    }
  }

  return (
    <div className="flex items-center justify-between">
      {/* Status Indicator */}
      <div className="flex items-center gap-3">
        <div className={`w-3 h-3 rounded-full ${
          systemStatus.sentry_running ? 'bg-green-400' : 'bg-red-400'
        } animate-pulse shadow-lg`}></div>
        <span className="text-sm font-medium text-slate-600">
          {systemStatus.loading ? 'Checking status...' : (
            systemStatus.sentry_running ? 'Sentry Active' : 'Sentry Stopped'
          )}
        </span>
      </div>

      {/* Toggle Button */}
      <button
        onClick={handleToggle}
        disabled={actionLoading || !systemStatus.sentry_available}
        className={`px-6 py-2.5 rounded-xl font-medium transition-all ${
          !systemStatus.sentry_available
            ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
            : systemStatus.sentry_running
              ? 'bg-red-500 text-white hover:bg-red-600 active:scale-95 shadow-sm hover:shadow-md'
              : 'bg-green-500 text-white hover:bg-green-600 active:scale-95 shadow-sm hover:shadow-md'
        }`}
      >
        {actionLoading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span>{systemStatus.sentry_running ? 'Stopping...' : 'Starting...'}</span>
          </span>
        ) : (
          <span className="flex items-center justify-center gap-2">
            {systemStatus.sentry_running ? (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 10a1 1 0 011-1h4a1 1 0 011 1v4a1 1 0 01-1 1h-4a1 1 0 01-1-1v-4z" />
                </svg>
                Stop Sentry
              </>
            ) : (
              <>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Start Sentry
              </>
            )}
          </span>
        )}
      </button>

      {/* Error Message */}
      {!systemStatus.sentry_available && (
        <div className="ml-4 text-sm text-yellow-600">
          ⚠️ Service unavailable
        </div>
      )}
    </div>
  )
}

export default SystemControls
