import React, { useState, useEffect, useCallback, useRef } from 'react';
import {
  View,
  Text,
  FlatList,
  RefreshControl,
  StyleSheet,
  ActivityIndicator,
  TouchableOpacity,
  Animated,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import EventCard from '../components/EventCard';
import EventDetail from '../components/EventDetail';
import ApiService from '../services/api.service';
import { API_CONFIG } from '../config/api.config';

/**
 * ActivityLogScreen Component
 * Main screen displaying real-time activity logs with polling
 */
const ActivityLogScreen = () => {
  const [events, setEvents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [detailVisible, setDetailVisible] = useState(false);
  const [isLive, setIsLive] = useState(true);

  // Polling interval ref
  const pollingInterval = useRef(null);

  // Animation for live indicator
  const pulseAnim = useRef(new Animated.Value(1)).current;

  /**
   * Fetch events from API
   */
  const fetchEvents = async (showLoading = true) => {
    try {
      if (showLoading) {
        setLoading(true);
      }
      setError(null);

      const data = await ApiService.getEvents(API_CONFIG.DEFAULT_LIMIT);
      setEvents(data);
      setIsLive(true);
    } catch (err) {
      console.error('Error fetching events:', err);
      setError(err.message || 'Failed to fetch events');
      setIsLive(false);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  /**
   * Handle pull-to-refresh
   */
  const onRefresh = useCallback(() => {
    setRefreshing(true);
    fetchEvents(false);
  }, []);

  /**
   * Handle event card press
   */
  const handleEventPress = (event) => {
    setSelectedEvent(event);
    setDetailVisible(true);
  };

  /**
   * Close event detail modal
   */
  const handleCloseDetail = () => {
    setDetailVisible(false);
    setTimeout(() => setSelectedEvent(null), 300);
  };

  /**
   * Start polling for new events
   */
  const startPolling = () => {
    if (pollingInterval.current) {
      clearInterval(pollingInterval.current);
    }

    pollingInterval.current = setInterval(() => {
      fetchEvents(false);
    }, API_CONFIG.POLLING_INTERVAL);
  };

  /**
   * Stop polling
   */
  const stopPolling = () => {
    if (pollingInterval.current) {
      clearInterval(pollingInterval.current);
      pollingInterval.current = null;
    }
  };

  /**
   * Pulse animation for live indicator
   */
  const startPulseAnimation = () => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(pulseAnim, {
          toValue: 1.3,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(pulseAnim, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  };

  /**
   * Initialize on mount
   */
  useEffect(() => {
    fetchEvents();
    startPolling();
    startPulseAnimation();

    return () => {
      stopPolling();
    };
  }, []);

  /**
   * Render empty state
   */
  const renderEmptyState = () => {
    if (loading) {
      return (
        <View style={styles.centerContainer}>
          <ActivityIndicator size="large" color="#3B82F6" />
          <Text style={styles.loadingText}>Loading activity logs...</Text>
        </View>
      );
    }

    if (error) {
      return (
        <View style={styles.centerContainer}>
          <Text style={styles.errorIcon}>⚠️</Text>
          <Text style={styles.errorTitle}>Connection Error</Text>
          <Text style={styles.errorMessage}>{error}</Text>
          <Text style={styles.errorHint}>
            Make sure the backend is running and accessible
          </Text>
          <TouchableOpacity
            style={styles.retryButton}
            onPress={() => fetchEvents()}
          >
            <Text style={styles.retryButtonText}>Retry</Text>
          </TouchableOpacity>
        </View>
      );
    }

    return (
      <View style={styles.centerContainer}>
        <Text style={styles.emptyIcon}>📋</Text>
        <Text style={styles.emptyTitle}>No Events Yet</Text>
        <Text style={styles.emptyMessage}>
          Activity logs will appear here when events are detected
        </Text>
      </View>
    );
  };

  /**
   * Render header
   */
  const renderHeader = () => (
    <View style={styles.header}>
      <View style={styles.headerTop}>
        <Text style={styles.title}>Activity Log</Text>
        <View style={styles.liveIndicator}>
          <Animated.View
            style={[
              styles.liveDot,
              {
                backgroundColor: isLive ? '#10B981' : '#9CA3AF',
                transform: [{ scale: isLive ? pulseAnim : 1 }],
              },
            ]}
          />
          <Text style={styles.liveText}>
            {isLive ? 'LIVE' : 'OFFLINE'}
          </Text>
        </View>
      </View>
      <View style={styles.statsContainer}>
        <View style={styles.statItem}>
          <Text style={styles.statValue}>{events.length}</Text>
          <Text style={styles.statLabel}>Events</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statValue}>
            {events.filter(e => e.severity === 'critical').length}
          </Text>
          <Text style={[styles.statLabel, { color: '#DC2626' }]}>Critical</Text>
        </View>
        <View style={styles.statDivider} />
        <View style={styles.statItem}>
          <Text style={styles.statValue}>
            {events.filter(e => e.severity === 'warning').length}
          </Text>
          <Text style={[styles.statLabel, { color: '#F59E0B' }]}>Warning</Text>
        </View>
      </View>
    </View>
  );

  /**
   * Render event item
   */
  const renderItem = ({ item }) => (
    <EventCard event={item} onPress={handleEventPress} />
  );

  /**
   * Key extractor
   */
  const keyExtractor = (item) => item.id?.toString() || Math.random().toString();

  return (
    <View style={styles.container}>
      <StatusBar style="dark" />

      {renderHeader()}

      <FlatList
        data={events}
        renderItem={renderItem}
        keyExtractor={keyExtractor}
        contentContainerStyle={styles.listContent}
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
            tintColor="#3B82F6"
            colors={['#3B82F6']}
          />
        }
        ListEmptyComponent={renderEmptyState}
      />

      {/* Event Detail Modal */}
      <EventDetail
        visible={detailVisible}
        event={selectedEvent}
        onClose={handleCloseDetail}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F4F6',
  },
  header: {
    backgroundColor: '#FFFFFF',
    paddingTop: 60,
    paddingBottom: 16,
    paddingHorizontal: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#E5E7EB',
  },
  headerTop: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  title: {
    fontSize: 32,
    fontWeight: '700',
    color: '#111827',
  },
  liveIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: '#F9FAFB',
    borderRadius: 16,
  },
  liveDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 6,
  },
  liveText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#6B7280',
    letterSpacing: 0.5,
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    backgroundColor: '#F9FAFB',
    borderRadius: 12,
    padding: 12,
  },
  statItem: {
    flex: 1,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: '700',
    color: '#111827',
    marginBottom: 2,
  },
  statLabel: {
    fontSize: 11,
    fontWeight: '600',
    color: '#6B7280',
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  statDivider: {
    width: 1,
    backgroundColor: '#E5E7EB',
    marginHorizontal: 8,
  },
  listContent: {
    paddingVertical: 12,
    flexGrow: 1,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#6B7280',
    fontWeight: '500',
  },
  errorIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  errorTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: '#111827',
    marginBottom: 8,
  },
  errorMessage: {
    fontSize: 16,
    color: '#DC2626',
    textAlign: 'center',
    marginBottom: 8,
  },
  errorHint: {
    fontSize: 14,
    color: '#6B7280',
    textAlign: 'center',
    marginBottom: 24,
  },
  retryButton: {
    backgroundColor: '#3B82F6',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  retryButtonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '600',
  },
  emptyIcon: {
    fontSize: 64,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: '#111827',
    marginBottom: 8,
  },
  emptyMessage: {
    fontSize: 16,
    color: '#6B7280',
    textAlign: 'center',
  },
});

export default ActivityLogScreen;
