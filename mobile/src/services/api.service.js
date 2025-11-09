import axios from 'axios';
import { API_CONFIG } from '../config/api.config';

// Create axios instance with base configuration
const apiClient = axios.create({
  baseURL: API_CONFIG.BASE_URL,
  timeout: API_CONFIG.TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.message);
    if (error.response) {
      // Server responded with error status
      console.error('Error Status:', error.response.status);
      console.error('Error Data:', error.response.data);
    } else if (error.request) {
      // Request was made but no response received
      console.error('No response received from server');
    }
    return Promise.reject(error);
  }
);

/**
 * API Service for SharkBytes Security System
 */
export const ApiService = {
  /**
   * Fetch events/activity logs
   * @param {number} limit - Number of events to fetch (default: 50)
   * @param {string} eventType - Filter by event type (optional)
   * @returns {Promise<Array>} Array of events
   */
  async getEvents(limit = API_CONFIG.DEFAULT_LIMIT, eventType = null) {
    try {
      const params = { limit };
      if (eventType) {
        params.event_type = eventType;
      }

      const response = await apiClient.get('/events', { params });

      // Transform snake_case to camelCase for consistency
      return response.data.map(event => ({
        id: event.id,
        timestamp: event.timestamp,
        eventType: event.event_type,
        description: event.description,
        severity: event.severity,
        imageUrl: event.image_url,
      }));
    } catch (error) {
      console.error('Failed to fetch events:', error);
      throw error;
    }
  },

  /**
   * Fetch anomalies (alias for getEvents)
   * @param {number} limit - Number of anomalies to fetch
   * @returns {Promise<Array>} Array of anomalies
   */
  async getAnomalies(limit = API_CONFIG.DEFAULT_LIMIT) {
    try {
      const response = await apiClient.get('/anomalies', {
        params: { limit }
      });

      return response.data.map(event => ({
        id: event.id,
        timestamp: event.timestamp,
        eventType: event.event_type,
        description: event.description,
        severity: event.severity,
        imageUrl: event.image_url,
      }));
    } catch (error) {
      console.error('Failed to fetch anomalies:', error);
      throw error;
    }
  },

  /**
   * Create a new event
   * @param {Object} eventData - Event data
   * @param {string} eventData.eventType - Type of event
   * @param {string} eventData.description - Event description
   * @param {string} eventData.severity - Severity level (info, warning, critical)
   * @returns {Promise<Object>} Created event
   */
  async createEvent(eventData) {
    try {
      const payload = {
        event_type: eventData.eventType,
        description: eventData.description,
        severity: eventData.severity || 'info',
      };

      const response = await apiClient.post('/events', payload);

      return {
        id: response.data.id,
        timestamp: response.data.timestamp,
        eventType: response.data.event_type,
        description: response.data.description,
        severity: response.data.severity,
        imageUrl: response.data.image_url,
      };
    } catch (error) {
      console.error('Failed to create event:', error);
      throw error;
    }
  },

  /**
   * Check backend health status
   * @returns {Promise<Object>} Health status
   */
  async healthCheck() {
    try {
      const response = await apiClient.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  /**
   * Send camera control command
   * @param {string} command - Control command
   * @returns {Promise<Object>} Command response
   */
  async sendControlCommand(command) {
    try {
      const response = await apiClient.post('/control', { command });
      return response.data;
    } catch (error) {
      console.error('Failed to send control command:', error);
      throw error;
    }
  },

  /**
   * Get system status
   * @returns {Promise<Object>} System status
   */
  async getSystemStatus() {
    try {
      const response = await apiClient.get('/system/status');
      return response.data;
    } catch (error) {
      console.error('Failed to get system status:', error);
      throw error;
    }
  },

  /**
   * Start the sentry system
   * @returns {Promise<Object>} Start response
   */
  async startSystem() {
    try {
      const response = await apiClient.post('/system/start');
      return response.data;
    } catch (error) {
      console.error('Failed to start system:', error);
      throw error;
    }
  },

  /**
   * Stop the sentry system
   * @returns {Promise<Object>} Stop response
   */
  async stopSystem() {
    try {
      const response = await apiClient.post('/system/stop');
      return response.data;
    } catch (error) {
      console.error('Failed to stop system:', error);
      throw error;
    }
  },
};

export default ApiService;
