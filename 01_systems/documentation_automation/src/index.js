/**
 * Documentation Automation System
 * AI-powered documentation generation and maintenance
 */

const express = require('express');
const config = require('./config');
const { logger } = require('./utils/logger');
const { documentation_automationService } = require('./services/documentation_automationService');

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'documentation_automation',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// API Routes
app.get('/api/v1/status', async (req, res) => {
  try {
    const status = await documentation_automationService.getStatus();
    res.json(status);
  } catch (error) {
    logger.error('Error getting status:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/v1/process', async (req, res) => {
  try {
    const result = await documentation_automationService.process(req.body);
    res.json(result);
  } catch (error) {
    logger.error('Error processing request:', error);
    res.status(500).json({ error: 'Processing failed' });
  }
});

// Start server
const PORT = config.port || 3000;
app.listen(PORT, () => {
  logger.info(`Documentation Automation System running on port ${PORT}`);
});

module.exports = app;
