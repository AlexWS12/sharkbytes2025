import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ActivityIndicator,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import { StatusBar } from 'expo-status-bar';
import { Ionicons } from '@expo/vector-icons';
import { Image } from 'expo-image';
import ApiService from '../services/api.service';
import { API_CONFIG } from '../config/api.config';

const { width } = Dimensions.get('window');

/**
 * LiveFeedScreen Component
 * Displays live video feed from the sentry camera
 */
const LiveFeedScreen = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [systemStatus, setSystemStatus] = useState({
    sentry_running: false,
    sentry_available: false,
  });
  const [stats, setStats] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);

  // Video feed URL with timestamp to prevent caching
  const [feedUrl, setFeedUrl] = useState('');

  /**
   * Fetch system status
   */
  const fetchSystemStatus = async () => {
    try {
      const status = await ApiService.getSystemStatus();
      setSystemStatus({
        sentry_running: status.sentry_running,
        sentry_available: status.sentry_available,
      });
      setStats(status.stats);
      setError(null);
    } catch (err) {
      console.error('Error fetching system status:', err);
      setError('Unable to connect to backend');
    }
  };

  /**
   * Toggle sentry start/stop
   */
  const handleToggleSentry = async () => {
    setActionLoading(true);
    try {
      if (systemStatus.sentry_running) {
        await ApiService.stopSystem();
      } else {
        await ApiService.startSystem();
      }
      await fetchSystemStatus();
    } catch (err) {
      console.error('Error toggling system:', err);
      setError(err.message || 'Failed to toggle system');
    } finally {
      setActionLoading(false);
    }
  };

  /**
   * Update feed URL to prevent caching
   */
  useEffect(() => {
    const updateFeedUrl = () => {
      setFeedUrl(`${API_CONFIG.BASE_URL}/video_feed?t=${Date.now()}`);
    };

    updateFeedUrl();
    const interval = setInterval(updateFeedUrl, 100); // Refresh URL every 100ms

    return () => clearInterval(interval);
  }, []);

  /**
   * Poll for status updates
   */
  useEffect(() => {
    fetchSystemStatus();
    const interval = setInterval(fetchSystemStatus, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      <StatusBar style="dark" />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Live Feed</Text>
        
        {/* Start/Stop Button */}
        <TouchableOpacity
          style={[
            styles.toggleButton,
            systemStatus.sentry_running ? styles.stopButton : styles.startButton,
            !systemStatus.sentry_available && styles.disabledButton,
          ]}
          onPress={handleToggleSentry}
          disabled={actionLoading || !systemStatus.sentry_available}
        >
          {actionLoading ? (
            <ActivityIndicator size="small" color="#fff" />
          ) : (
            <Ionicons 
              name={systemStatus.sentry_running ? 'stop' : 'play'} 
              size={20} 
              color="#fff" 
            />
          )}
        </TouchableOpacity>
      </View>

      {/* Video Feed Container */}
      <View style={styles.videoContainer}>
        {error ? (
          <View style={styles.errorContainer}>
            <Ionicons name="alert-circle-outline" size={64} color="#F59E0B" />
            <Text style={styles.errorText}>{error}</Text>
            <TouchableOpacity
              style={styles.retryButton}
              onPress={fetchSystemStatus}
            >
              <Text style={styles.retryButtonText}>Retry</Text>
            </TouchableOpacity>
          </View>
        ) : !systemStatus.sentry_running ? (
          <View style={styles.errorContainer}>
            <Ionicons name="videocam-off-outline" size={64} color="#6B7280" />
            <Text style={styles.errorText}>Camera Offline</Text>
            <Text style={styles.errorHint}>Press play to start the sentry</Text>
          </View>
        ) : (
          <>
            <Image
              source={{ uri: feedUrl }}
              style={styles.videoFeed}
              contentFit="contain"
              cachePolicy="none"
              onLoadStart={() => setLoading(true)}
              onLoad={() => setLoading(false)}
              onError={(e) => {
                setLoading(false);
                console.error('Video feed error:', e);
              }}
            />
            
            {loading && (
              <View style={styles.loadingOverlay}>
                <ActivityIndicator size="large" color="#35DDF9" />
              </View>
            )}

            {/* Overlay Stats */}
            <View style={styles.overlay}>
              <View style={styles.liveIndicator}>
                <View style={styles.liveDot} />
                <Text style={styles.liveText}>LIVE</Text>
              </View>

              {stats && (
                <View style={styles.statsOverlay}>
                  <View style={styles.statItem}>
                    <Text style={styles.statLabel}>STATUS</Text>
                    <Text style={styles.statValue}>{stats.tracking_status}</Text>
                  </View>
                  <View style={styles.statItem}>
                    <Text style={styles.statLabel}>FPS</Text>
                    <Text style={styles.statValue}>{Math.round(stats.fps)}</Text>
                  </View>
                  <View style={styles.statItem}>
                    <Text style={styles.statLabel}>TRACKS</Text>
                    <Text style={styles.statValue}>{stats.people_count}</Text>
                  </View>
                </View>
              )}
            </View>
          </>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0A0F1A',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 60,
    paddingHorizontal: 20,
    paddingBottom: 16,
    backgroundColor: '#0D1117',
    borderBottomWidth: 1,
    borderBottomColor: '#35DDF9',
    borderBottomOpacity: 0.2,
  },
  title: {
    fontSize: 28,
    fontWeight: '700',
    color: '#35DDF9',
  },
  toggleButton: {
    width: 50,
    height: 50,
    borderRadius: 25,
    justifyContent: 'center',
    alignItems: 'center',
  },
  startButton: {
    backgroundColor: '#35DDF9',
  },
  stopButton: {
    backgroundColor: '#EF4444',
  },
  disabledButton: {
    backgroundColor: '#4B5563',
  },
  videoContainer: {
    flex: 1,
    backgroundColor: '#000000',
    justifyContent: 'center',
    alignItems: 'center',
  },
  videoFeed: {
    width: '100%',
    height: '100%',
  },
  loadingOverlay: {
    ...StyleSheet.absoluteFillObject,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  overlay: {
    position: 'absolute',
    top: 16,
    left: 16,
    right: 16,
  },
  liveIndicator: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    alignSelf: 'flex-start',
    borderWidth: 1,
    borderColor: 'rgba(53, 221, 249, 0.4)',
  },
  liveDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: '#35DDF9',
    marginRight: 8,
  },
  liveText: {
    fontSize: 12,
    fontWeight: '700',
    color: '#35DDF9',
    letterSpacing: 1,
  },
  statsOverlay: {
    flexDirection: 'row',
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 8,
    marginTop: 8,
    borderWidth: 1,
    borderColor: 'rgba(53, 221, 249, 0.4)',
    gap: 16,
  },
  statItem: {
    alignItems: 'center',
  },
  statLabel: {
    fontSize: 10,
    fontWeight: '700',
    color: '#35DDF9',
    marginBottom: 2,
  },
  statValue: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  errorContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  errorText: {
    fontSize: 18,
    fontWeight: '600',
    color: '#E5E7EB',
    marginBottom: 8,
    textAlign: 'center',
  },
  errorHint: {
    fontSize: 14,
    color: '#9CA3AF',
    textAlign: 'center',
  },
  retryButton: {
    marginTop: 20,
    paddingHorizontal: 24,
    paddingVertical: 12,
    backgroundColor: '#35DDF9',
    borderRadius: 8,
  },
  retryButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#000000',
  },
});

export default LiveFeedScreen;
