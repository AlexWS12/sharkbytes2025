// API Configuration
// Update this with your actual backend URL
// For local development, use your computer's IP address (not localhost)
// Example: 'http://192.168.1.100:8000'

export const API_CONFIG = {
  BASE_URL: 'http://192.168.1.154:5000', // Change to your IP address for device testing
  POLLING_INTERVAL: 5000, // 5 seconds
  DEFAULT_LIMIT: 50,
  TIMEOUT: 10000, // 10 seconds
};

// For iOS Simulator, you can use localhost
// For physical device, use your computer's IP address:
// 1. Run `ifconfig` (Mac/Linux) or `ipconfig` (Windows)
// 2. Find your local IP (usually starts with 192.168.x.x)
// 3. Update BASE_URL to: 'http://192.168.x.x:8000'
