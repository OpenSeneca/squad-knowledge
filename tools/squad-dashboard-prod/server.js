#!/usr/bin/env node
/**
 * Squad Dashboard - Production-Ready Monitoring
 * 
 * Monitors all 4 squad agents (marcus, archimedes, argus, galen)
 * with status, last output, uptime, activity.
 * 
 * Auto-updates every 5 minutes.
 * 
 * Deployed as systemd service on forge (100.93.69.117)
 * Uses squad-output data from ~/.openclaw/squad-output/
 */

const express = require('express');
const fs = require('fs').promises;
const path = require('path');

const PORT = process.env.PORT || 3000;
const UPDATE_INTERVAL = 5 * 60 * 1000; // 5 minutes in milliseconds
const SQUAD_OUTPUT_BASE = '/home/exedev/.openclaw/squad-output';

// Squad agents to monitor
const AGENTS = ['marcus', 'archimedes', 'argus', 'galen'];

// In-memory cache
let agentData = {};
let lastUpdateTime = null;

class DashboardServer {
    constructor() {
        this.app = express();
        this.setupMiddleware();
        this.setupRoutes();
    }

    setupMiddleware() {
        this.app.use(express.json());
        this.app.use((req, res, next) => {
            res.header('Access-Control-Allow-Origin', '*');
            res.header('Access-Control-Allow-Methods', 'GET, OPTIONS');
            res.header('Access-Control-Allow-Headers', 'Content-Type');
            next();
        });
    }

    setupRoutes() {
        // Health check
        this.app.get('/api/health', (req, res) => {
            res.json({
                status: 'healthy',
                server: 'squad-dashboard-prod',
                version: '1.0.0',
                uptime: this.getUptime(),
                lastUpdate: lastUpdateTime,
                agentsCount: Object.keys(agentData).length
            });
        });

        // Full dashboard data
        this.app.get('/api/status', async (req, res) => {
            try {
                await this.loadAgentData();
                const data = {
                    updated: new Date().toISOString(),
                    agents: AGENTS.map(agent => ({
                        name: agent,
                        ...this.getAgentInfo(agent)
                    }))
                };
                res.json(data);
            } catch (error) {
                console.error('Error loading agent data:', error);
                res.status(500).json({ error: 'Failed to load agent data' });
            }
        });

        // Individual agent status
        this.app.get('/api/agent/:name', async (req, res) => {
            const agentName = req.params.name.toLowerCase();
            if (!AGENTS.includes(agentName)) {
                return res.status(404).json({ error: 'Agent not found' });
            }
            
            try {
                await this.loadAgentData(agentName);
                res.json({
                    name: agentName,
                    ...this.getAgentInfo(agentName)
                });
            } catch (error) {
                console.error(`Error loading ${agentName} data:`, error);
                res.status(500).json({ error: 'Failed to load agent data' });
            }
        });

        // Static files for web UI
        this.app.use(express.static(path.join(__dirname, 'public')));
    }

    async loadAgentData(agentName) {
        const agentPath = path.join(SQUAD_OUTPUT_BASE, agentName);
        
        // Read agent files
        const learningsPath = path.join(agentPath, 'learnings');
        const memoryPath = path.join(agentPath, 'memory');
        const workspacePath = path.join(agentPath, 'workspace');
        
        const agentInfo = {
            status: 'unknown',
            lastOutput: null,
            lastUpdate: null,
            uptime: null,
            activity: []
        };

        try {
            // Try to get status from various sources
            const files = await fs.readdir(agentPath).catch(() => []);
            
            // Check for status indicators
            if (files.includes('status.json')) {
                const statusContent = await fs.readFile(path.join(agentPath, 'status.json'), 'utf8');
                const statusData = JSON.parse(statusContent);
                agentInfo.status = statusData.status || 'active';
                agentInfo.lastUpdate = statusData.lastUpdate || null;
            } else if (files.length > 0) {
                agentInfo.status = 'active';
            }
            
            // Get last output from learnings
            const learningsFiles = await fs.readdir(learningsPath).catch(() => []);
            if (learningsFiles.length > 0) {
                const latestLearning = learningsFiles
                    .filter(f => f.endsWith('.md'))
                    .sort()
                    .pop();
                
                if (latestLearning) {
                    const learningContent = await fs.readFile(path.join(learningsPath, latestLearning), 'utf8');
                    const lines = learningContent.split('\\n').filter(l => l.trim());
                    agentInfo.lastOutput = lines.slice(-5).join('\\n'); // Last 5 lines
                }
            }
            
            // Calculate uptime (simplified - last activity)
            if (agentInfo.lastUpdate) {
                const lastUpdate = new Date(agentInfo.lastUpdate);
                const now = new Date();
                const diffHours = (now - lastUpdate) / (1000 * 60 * 60);
                agentInfo.uptime = `${diffHours.toFixed(1)} hours ago`;
            }
            
            // Get recent activity
            agentInfo.activity = await this.getRecentActivity(agentPath);
            
            agentData[agentName] = agentInfo;
            
        } catch (error) {
            console.error(`Error loading data for ${agentName}:`, error);
            agentInfo.status = 'error';
            agentInfo.activity = [{ type: 'error', message: error.message }];
            agentData[agentName] = agentInfo;
        }
    }

    async loadAgentData(agentName) {
        if (agentData[agentName] && Date.now() - new Date(lastUpdateTime).getTime() < UPDATE_INTERVAL) {
            return; // Use cache if within update interval
        }
        
        await this.loadAgentData(agentName);
        lastUpdateTime = new Date().toISOString();
    }

    async loadAgentData() {
        await Promise.all(AGENTS.map(agent => this.loadAgentData(agent)));
        lastUpdateTime = new Date().toISOString();
    }

    async getRecentActivity(agentPath) {
        const activity = [];
        
        try {
            // Check learnings for recent activity
            const learningsPath = path.join(agentPath, 'learnings');
            const learningsFiles = await fs.readdir(learningsPath).catch(() => []);
            
            for (const file of learningsFiles.slice(-3)) { // Last 3 files
                const stats = await fs.stat(path.join(learningsPath, file));
                activity.push({
                    type: 'learning',
                    file: file,
                    timestamp: stats.mtime.toISOString()
                });
            }
            
            // Check memory
            const memoryPath = path.join(agentPath, 'memory');
            const memoryFiles = await fs.readdir(memoryPath).catch(() => []);
            for (const file of memoryFiles.slice(-3)) {
                const stats = await fs.stat(path.join(memoryPath, file));
                activity.push({
                    type: 'memory',
                    file: file,
                    timestamp: stats.mtime.toISOString()
                });
            }
            
        } catch (error) {
            console.error('Error getting recent activity:', error);
        }
        
        return activity.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 10);
    }

    getAgentInfo(agentName) {
        return agentData[agentName] || {
            name: agentName,
            status: 'unknown',
            lastOutput: 'No data available',
            lastUpdate: null,
            uptime: 'Unknown',
            activity: []
        };
    }

    getUptime() {
        if (!lastUpdateTime) return 'N/A';
        const uptime = Date.now() - new Date(lastUpdateTime).getTime();
        const minutes = Math.floor(uptime / (1000 * 60));
        const hours = Math.floor(minutes / 60);
        return `${hours}h ${minutes % 60}m`;
    }

    async startAutoUpdate() {
        console.log(`Starting auto-update every ${UPDATE_INTERVAL / 1000 / 60} minutes`);
        
        setInterval(async () => {
            try {
                console.log('Auto-updating agent data...');
                await this.loadAgentData();
                console.log('Auto-update completed');
            } catch (error) {
                console.error('Auto-update error:', error);
            }
        }, UPDATE_INTERVAL);
    }

    start() {
        this.app.listen(PORT, () => {
            console.log(`Squad Dashboard running on port ${PORT}`);
            console.log(`Monitoring agents: ${AGENTS.join(', ')}`);
            console.log(`Auto-update interval: ${UPDATE_INTERVAL / 1000 / 60} minutes`);
            console.log(`Squad output base: ${SQUAD_OUTPUT_BASE}`);
        });

        // Initial load
        this.loadAgentData().then(() => {
            lastUpdateTime = new Date().toISOString();
            console.log('Initial agent data loaded');
        }).catch(error => {
            console.error('Error in initial load:', error);
        });

        // Start auto-update
        this.startAutoUpdate();
    }
}

// Start server
const server = new DashboardServer();
server.start();

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('Received SIGTERM, shutting down gracefully...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('Received SIGINT, shutting down gracefully...');
    process.exit(0);
});
