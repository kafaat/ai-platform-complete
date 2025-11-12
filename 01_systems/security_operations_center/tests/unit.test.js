/**
 * Unit tests for Security Operations Center (SOC)
 */

const { security_operations_centerService } = require('../src/services/security_operations_centerService');

describe('Security Operations Center (SOC)', () => {
  test('should initialize successfully', async () => {
    await security_operations_centerService.initialize();
    expect(security_operations_centerService.initialized).toBe(true);
  });
  
  test('should return status', async () => {
    const status = await security_operations_centerService.getStatus();
    expect(status).toHaveProperty('service');
    expect(status).toHaveProperty('status');
    expect(status).toHaveProperty('timestamp');
  });
  
  test('should process data successfully', async () => {
    const result = await security_operations_centerService.process({ test: 'data' });
    expect(result.success).toBe(true);
  });
});
