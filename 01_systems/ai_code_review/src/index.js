/**
 * AI Code Review System
 * Automated code quality and security analysis
 */

const express = require('express');
const config = require('./config');
const { logger } = require('./utils/logger');
const { ai_code_reviewService } = require('./services/ai_code_reviewService');

const app = express();

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'ai_code_review',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// API Routes
app.get('/api/v1/status', async (req, res) => {
  try {
    const status = await ai_code_reviewService.getStatus();
    res.json(status);
  } catch (error) {
    logger.error('Error getting status:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

app.post('/api/v1/process', async (req, res) => {
  try {
    const result = await ai_code_reviewService.process(req.body);
    res.json(result);
  } catch (error) {
    logger.error('Error processing request:', error);
    res.status(500).json({ error: 'Processing failed' });
  }
});

// Start server
const PORT = config.port || 3000;
app.listen(PORT, () => {
  logger.info(`AI Code Review System running on port ${PORT}`);
});

module.exports = app;
