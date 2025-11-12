/**
 * Unit tests for AI Code Review System
 */

const { ai_code_reviewService } = require('../src/services/ai_code_reviewService');

describe('AI Code Review System', () => {
  test('should initialize successfully', async () => {
    await ai_code_reviewService.initialize();
    expect(ai_code_reviewService.initialized).toBe(true);
  });
  
  test('should return status', async () => {
    const status = await ai_code_reviewService.getStatus();
    expect(status).toHaveProperty('service');
    expect(status).toHaveProperty('status');
    expect(status).toHaveProperty('timestamp');
  });
  
  test('should process data successfully', async () => {
    const result = await ai_code_reviewService.process({ test: 'data' });
    expect(result.success).toBe(true);
  });
});
