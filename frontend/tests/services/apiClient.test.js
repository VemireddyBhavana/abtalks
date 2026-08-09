import { describe, it, expect } from 'vitest';
import apiClient, { sanitizeInput } from '../../src/services/apiClient';

describe('apiClient Service', () => {
  it('should create axios instance with default 15s timeout', () => {
    expect(apiClient.defaults.timeout).toBe(15000);
  });

  it('should sanitize input strings to prevent XSS', () => {
    const raw = '<script>alert("xss")</script>';
    const sanitized = sanitizeInput(raw);
    expect(sanitized).toBe('&lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;');
  });

  it('should return raw input if not a string', () => {
    expect(sanitizeInput(123)).toBe(123);
  });
});
