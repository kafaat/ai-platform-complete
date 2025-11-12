/**
 * Cloud Cost Optimization Platform
 * ML-driven cloud resource optimization and cost management
 */

const express = require('express');
const config = require('./config');
const { logger } = require('./utils/logger');
const { cloud_cost_optimizationService } = require('./services/cloud_cost_optimizationService');

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'cloud_cost_optimization',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// API Routes
app.get('/api/v1/status', async (req, res) => {
  try {
    const status = await cloud_cost_optimizationService.getStatus();
    res.json(status);
  } catch (error) {
    logger.error('Error getting status:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/v1/process', async (req, res) => {
  try {
    const result = await cloud_cost_optimizationService.process(req.body);
    res.json(result);
  } catch (error) {
    logger.error('Error processing request:', error);
    res.status(500).json({ error: 'Processing failed' });
  }
});

// Start server
const PORT = config.port || 3000;
app.listen(PORT, () => {
  logger.info(`Cloud Cost Optimization Platform running on port ${PORT}`);
});

module.exports = app;
