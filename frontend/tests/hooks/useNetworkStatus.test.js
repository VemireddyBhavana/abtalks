import { describe, it, expect } from 'vitest';
import { renderHook } from '@testing-library/react';
import { useNetworkStatus } from '../../src/hooks/useNetworkStatus';

describe('useNetworkStatus Hook', () => {
  it('should return initial online status', () => {
    const { result } = renderHook(() => useNetworkStatus());
    expect(result.current.isOnline).toBe(navigator.onLine);
    expect(result.current.wasOffline).toBe(false);
  });
});
