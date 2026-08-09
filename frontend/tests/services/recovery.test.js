import { describe, it, expect, beforeEach } from 'vitest';
import { sessionRecovery } from '../../src/services/sessionRecovery';

describe('sessionRecovery Service', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should return null when no session ID is stored', () => {
    expect(sessionRecovery.getActiveSessionId()).toBeNull();
  });

  it('should store and retrieve active session ID correctly', () => {
    sessionRecovery.setActiveSessionId('sess_recovery_123');
    expect(sessionRecovery.getActiveSessionId()).toBe('sess_recovery_123');
  });

  it('should clear active session ID upon invalidation', () => {
    sessionRecovery.setActiveSessionId('sess_recovery_456');
    sessionRecovery.clearActiveSession();
    expect(sessionRecovery.getActiveSessionId()).toBeNull();
  });
});
