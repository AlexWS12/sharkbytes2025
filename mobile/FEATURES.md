# SharkBytes Mobile - Features Overview

## App Features

### 🔴 Real-Time Monitoring
- **Auto-refresh**: Polls backend every 5 seconds for new events
- **Live indicator**: Animated pulse shows connection status
- **Background updates**: Continues fetching even when viewing details

### 📊 Activity Log Display
- **Card-based interface**: Clean, modern design
- **Severity color-coding**:
  - 🔵 **INFO** - Blue (normal activities)
  - 🟡 **WARNING** - Yellow (suspicious activities)
  - 🔴 **CRITICAL** - Red (immediate threats)
- **Smart timestamps**: Shows relative time (e.g., "5m ago", "2h ago")
- **Event thumbnails**: Preview images on each card
- **Event counter**: See total events at a glance

### 🔍 Detailed Event View
- **Full-screen modal**: Tap any event to see details
- **High-resolution images**: View captured frames in full quality
- **Complete metadata**:
  - Full timestamp (e.g., "Monday, November 8, 2025, 2:33:22 PM")
  - Event type
  - Severity level
  - Description
  - Event ID
- **Easy navigation**: Close with X button or swipe down

### 📈 Statistics Dashboard
- **Total events**: See count of all logged events
- **Critical events**: Quick view of urgent items
- **Warning events**: Track suspicious activities
- **Color-coded stats**: Matches severity colors

### 🔄 Pull-to-Refresh
- **Manual refresh**: Swipe down to reload instantly
- **Visual feedback**: Spinner shows refresh in progress
- **Smart loading**: Doesn't interfere with auto-refresh

### ⚠️ Error Handling
- **Connection errors**: Clear messages when backend is unreachable
- **Retry button**: Easy one-tap reconnection
- **Empty states**: Helpful messages when no events exist
- **Loading states**: Smooth transitions and spinners

### 📱 iOS Optimizations
- **Safe area support**: Works perfectly with notches and islands
- **Native feel**: Uses iOS design patterns
- **Smooth animations**: 60 FPS scrolling and transitions
- **Gesture support**: Pull-to-refresh, tap interactions

## Technical Features

### API Integration
- **RESTful client**: Axios-based HTTP client
- **Automatic retry**: Handles network failures gracefully
- **Request/response logging**: Debug-friendly console logs
- **Data transformation**: Converts snake_case to camelCase

### Performance
- **Efficient rendering**: FlatList with optimized key extraction
- **Image lazy loading**: Only loads visible images
- **Minimal re-renders**: Smart state management
- **Memory efficient**: Proper cleanup on unmount

### Architecture
- **Component-based**: Reusable, modular components
- **Service layer**: Centralized API logic
- **Configuration**: Easy-to-modify settings
- **Type safety**: Clear prop structures

## Component Breakdown

### ActivityLogScreen
**Main screen** - Orchestrates the entire activity log view
- Manages event state
- Handles polling lifecycle
- Renders header with stats
- Controls event list

### EventCard
**List item** - Individual event display
- Compact, scannable format
- Severity badge
- Relative timestamp
- Thumbnail preview
- Tap to expand

### EventDetail
**Modal view** - Full event information
- Full-screen presentation
- High-res image display
- Complete metadata
- Smooth animations

### ApiService
**API client** - Backend communication
- Centralized endpoints
- Error handling
- Data transformation
- Request logging

## Data Flow

```
Backend (FastAPI)
    ↓
/events endpoint
    ↓
ApiService.getEvents()
    ↓
ActivityLogScreen (polling every 5s)
    ↓
FlatList → EventCard
    ↓
Tap event
    ↓
EventDetail modal
```

## Severity Mapping

| Severity | Color | Use Case |
|----------|-------|----------|
| INFO | Blue (#3B82F6) | Normal operations, routine events |
| WARNING | Yellow (#F59E0B) | Suspicious activity, concerns |
| CRITICAL | Red (#DC2626) | Immediate threats, emergencies |

## Event Data Structure

Each event contains:
```javascript
{
  id: 123,                    // Unique identifier
  timestamp: "2025-11-08...", // ISO 8601 datetime
  eventType: "vision_analysis", // Type of event
  description: "Person detected...", // Human-readable description
  severity: "info",           // Severity level
  imageUrl: "https://..."     // Optional image URL
}
```

## Customization Options

### Polling Interval
Default: 5000ms (5 seconds)
```javascript
// src/config/api.config.js
POLLING_INTERVAL: 3000, // 3 seconds
```

### Event Limit
Default: 50 events
```javascript
// src/config/api.config.js
DEFAULT_LIMIT: 100, // Fetch 100 events
```

### Colors
Modify severity colors in:
- `EventCard.jsx` - `getSeverityColor()`
- `EventDetail.jsx` - `getSeverityColor()`
- `ActivityLogScreen.jsx` - Stat labels

### Timeouts
Default: 10 seconds
```javascript
// src/config/api.config.js
TIMEOUT: 15000, // 15 seconds
```

## Future Enhancements

Potential additions:
- [ ] Push notifications for critical events
- [ ] Filter by severity level
- [ ] Search events by description
- [ ] Export event logs
- [ ] Dark mode
- [ ] Event history charts
- [ ] Camera controls integration
- [ ] Video feed view
- [ ] Offline mode with local storage
- [ ] Biometric authentication
- [ ] Multiple camera support
- [ ] Event sharing

## Requirements

- iOS 13.0+
- Expo SDK 51
- React Native 0.74
- Backend API running on local network
- WiFi connection (phone and backend on same network)

## Browser Equivalent

This mobile app replicates the functionality of:
- Web frontend: [/frontend/src/components/AnomalyLog.jsx](../frontend/src/components/AnomalyLog.jsx:1)
- Same data source
- Same API endpoints
- Optimized for mobile UX
