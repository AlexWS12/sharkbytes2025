import React from 'react';
import {
  View,
  Text,
  Image,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
} from 'react-native';

const { width } = Dimensions.get('window');

/**
 * EventCard Component
 * Displays an individual event/activity log item
 */
const EventCard = ({ event, onPress }) => {
  /**
   * Format timestamp to readable format
   */
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return 'Unknown time';

    try {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / 60000);
      const diffHours = Math.floor(diffMs / 3600000);
      const diffDays = Math.floor(diffMs / 86400000);

      // Recent events - show relative time
      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays < 7) return `${diffDays}d ago`;

      // Older events - show date
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
      });
    } catch (error) {
      console.error('Error formatting timestamp:', error);
      return timestamp;
    }
  };

  /**
   * Get severity badge color
   */
  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return '#DC2626'; // Red
      case 'warning':
        return '#F59E0B'; // Amber
      case 'info':
      default:
        return '#3B82F6'; // Blue
    }
  };

  /**
   * Get severity badge text color
   */
  const getSeverityTextColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return '#FEE2E2'; // Light red
      case 'warning':
        return '#FEF3C7'; // Light amber
      case 'info':
      default:
        return '#DBEAFE'; // Light blue
    }
  };

  const severityColor = getSeverityColor(event.severity);
  const severityTextColor = getSeverityTextColor(event.severity);

  return (
    <TouchableOpacity
      style={[styles.card, { borderLeftColor: severityColor }]}
      onPress={() => onPress?.(event)}
      activeOpacity={0.7}
    >
      {/* Header Row */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <View
            style={[
              styles.severityBadge,
              { backgroundColor: severityColor + '20' }, // 20% opacity
            ]}
          >
            <Text
              style={[
                styles.severityText,
                { color: severityColor },
              ]}
            >
              {event.severity?.toUpperCase() || 'INFO'}
            </Text>
          </View>
          <Text style={styles.timestamp}>
            {formatTimestamp(event.timestamp)}
          </Text>
        </View>

        {event.imageUrl && (
          <View style={styles.imageIndicator}>
            <Text style={styles.imageIndicatorText}>📷</Text>
          </View>
        )}
      </View>

      {/* Description */}
      <Text style={styles.description} numberOfLines={3}>
        {event.description}
      </Text>

      {/* Event Type */}
      {event.eventType && (
        <Text style={styles.eventType}>
          {event.eventType.replace(/_/g, ' ')}
        </Text>
      )}

      {/* Thumbnail Image */}
      {event.imageUrl && (
        <View style={styles.thumbnailContainer}>
          <Image
            source={{ uri: event.imageUrl }}
            style={styles.thumbnail}
            resizeMode="cover"
          />
        </View>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginHorizontal: 16,
    marginVertical: 8,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  severityBadge: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 12,
    marginRight: 10,
  },
  severityText: {
    fontSize: 11,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  timestamp: {
    fontSize: 13,
    color: '#6B7280',
    fontWeight: '500',
  },
  imageIndicator: {
    width: 28,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#F3F4F6',
    justifyContent: 'center',
    alignItems: 'center',
  },
  imageIndicatorText: {
    fontSize: 14,
  },
  description: {
    fontSize: 15,
    lineHeight: 22,
    color: '#111827',
    marginBottom: 8,
  },
  eventType: {
    fontSize: 12,
    color: '#9CA3AF',
    fontWeight: '500',
    textTransform: 'capitalize',
    marginTop: 4,
  },
  thumbnailContainer: {
    marginTop: 12,
    borderRadius: 8,
    overflow: 'hidden',
    backgroundColor: '#F9FAFB',
  },
  thumbnail: {
    width: '100%',
    height: 180,
    backgroundColor: '#E5E7EB',
  },
});

export default EventCard;
