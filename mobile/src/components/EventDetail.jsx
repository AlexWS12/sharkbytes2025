import React, { useState } from 'react';
import {
  View,
  Text,
  Image,
  Modal,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  Dimensions,
  ActivityIndicator,
} from 'react-native';

const { width, height } = Dimensions.get('window');

/**
 * EventDetail Modal Component
 * Shows detailed view of a selected event with full-size image
 */
const EventDetail = ({ visible, event, onClose }) => {
  const [imageLoading, setImageLoading] = useState(true);

  if (!event) return null;

  /**
   * Format full timestamp
   */
  const formatFullTimestamp = (timestamp) => {
    if (!timestamp) return 'Unknown time';

    try {
      const date = new Date(timestamp);
      return date.toLocaleString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
      });
    } catch (error) {
      console.error('Error formatting timestamp:', error);
      return timestamp;
    }
  };

  /**
   * Get severity background color
   */
  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return '#DC2626';
      case 'warning':
        return '#F59E0B';
      case 'info':
      default:
        return '#3B82F6';
    }
  };

  /**
   * Get severity icon
   */
  const getSeverityIcon = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical':
        return '🚨';
      case 'warning':
        return '⚠️';
      case 'info':
      default:
        return 'ℹ️';
    }
  };

  const severityColor = getSeverityColor(event.severity);

  return (
    <Modal
      visible={visible}
      animationType="slide"
      presentationStyle="pageSheet"
      onRequestClose={onClose}
    >
      <View style={styles.container}>
        {/* Header */}
        <View style={[styles.header, { backgroundColor: severityColor }]}>
          <View style={styles.headerContent}>
            <Text style={styles.headerIcon}>
              {getSeverityIcon(event.severity)}
            </Text>
            <View style={styles.headerTextContainer}>
              <Text style={styles.headerTitle}>Event Details</Text>
              <Text style={styles.headerSubtitle}>
                ID: #{event.id}
              </Text>
            </View>
          </View>
          <TouchableOpacity
            style={styles.closeButton}
            onPress={onClose}
            hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}
          >
            <Text style={styles.closeButtonText}>✕</Text>
          </TouchableOpacity>
        </View>

        {/* Content */}
        <ScrollView
          style={styles.content}
          contentContainerStyle={styles.contentContainer}
          showsVerticalScrollIndicator={false}
        >
          {/* Severity Badge */}
          <View style={styles.section}>
            <View
              style={[
                styles.severityBadgeLarge,
                { backgroundColor: severityColor + '20' },
              ]}
            >
              <Text
                style={[
                  styles.severityTextLarge,
                  { color: severityColor },
                ]}
              >
                {event.severity?.toUpperCase() || 'INFO'}
              </Text>
            </View>
          </View>

          {/* Timestamp */}
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>TIMESTAMP</Text>
            <Text style={styles.timestampText}>
              {formatFullTimestamp(event.timestamp)}
            </Text>
          </View>

          {/* Event Type */}
          {event.eventType && (
            <View style={styles.section}>
              <Text style={styles.sectionLabel}>EVENT TYPE</Text>
              <Text style={styles.eventTypeText}>
                {event.eventType.replace(/_/g, ' ').toUpperCase()}
              </Text>
            </View>
          )}

          {/* Description */}
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>DESCRIPTION</Text>
            <Text style={styles.descriptionText}>
              {event.description}
            </Text>
          </View>

          {/* Image */}
          {event.imageUrl && (
            <View style={styles.section}>
              <Text style={styles.sectionLabel}>CAPTURED IMAGE</Text>
              <View style={styles.imageContainer}>
                {imageLoading && (
                  <View style={styles.imageLoader}>
                    <ActivityIndicator size="large" color={severityColor} />
                  </View>
                )}
                <Image
                  source={{ uri: event.imageUrl }}
                  style={styles.image}
                  resizeMode="contain"
                  onLoadStart={() => setImageLoading(true)}
                  onLoadEnd={() => setImageLoading(false)}
                />
              </View>
            </View>
          )}

          {/* Bottom spacing */}
          <View style={styles.bottomSpacer} />
        </ScrollView>
      </View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  header: {
    paddingTop: 50,
    paddingBottom: 20,
    paddingHorizontal: 20,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 4,
  },
  headerContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  headerIcon: {
    fontSize: 32,
    marginRight: 12,
  },
  headerTextContainer: {
    flex: 1,
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: '#FFFFFF',
    marginBottom: 2,
  },
  headerSubtitle: {
    fontSize: 14,
    color: '#FFFFFF',
    opacity: 0.9,
  },
  closeButton: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  closeButtonText: {
    fontSize: 24,
    color: '#FFFFFF',
    fontWeight: '300',
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
  },
  section: {
    marginBottom: 24,
  },
  sectionLabel: {
    fontSize: 11,
    fontWeight: '700',
    color: '#6B7280',
    letterSpacing: 1,
    marginBottom: 8,
  },
  severityBadgeLarge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 16,
  },
  severityTextLarge: {
    fontSize: 16,
    fontWeight: '700',
    letterSpacing: 1,
  },
  timestampText: {
    fontSize: 16,
    color: '#111827',
    fontWeight: '500',
  },
  eventTypeText: {
    fontSize: 16,
    color: '#111827',
    fontWeight: '600',
    letterSpacing: 0.5,
  },
  descriptionText: {
    fontSize: 17,
    lineHeight: 26,
    color: '#374151',
  },
  imageContainer: {
    width: '100%',
    height: height * 0.4,
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    overflow: 'hidden',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  imageLoader: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F3F4F6',
    zIndex: 1,
  },
  image: {
    width: '100%',
    height: '100%',
  },
  bottomSpacer: {
    height: 40,
  },
});

export default EventDetail;
