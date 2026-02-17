#!/usr/bin/env node

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 8000;
const DATA_FILE = path.join(__dirname, 'data.json');

// MIME types
const MIME_TYPES = {
    '.html': 'text/html',
    '.css': 'text/css',
    '.js': 'application/javascript',
    '.json': 'application/json',
    '.ico': 'image/x-icon',
};

// Load data.json
function loadData() {
    try {
        const data = fs.readFileSync(DATA_FILE, 'utf8');
        return JSON.parse(data);
    } catch (error) {
        console.error('Error loading data.json:', error);
        return { updated: new Date().toISOString(), agents: [] };
    }
}

// Serve static files
function serveStaticFile(filePath, res) {
    const ext = path.extname(filePath);
    const contentType = MIME_TYPES[ext] || 'text/plain';

    fs.readFile(filePath, (error, content) => {
        if (error) {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('404 Not Found');
            return;
        }

        res.writeHead(200, { 'Content-Type': contentType });
        res.end(content);
    });
}

// Create server
const server = http.createServer((req, res) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

    // Serve data.json API
    if (req.url === '/api/status' || req.url === '/api/status/') {
        const data = loadData();
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(data, null, 2));
        return;
    }

    // Serve index.html by default
    let filePath = path.join(__dirname, req.url === '/' ? 'index.html' : req.url.substring(1));

    // Security: prevent directory traversal
    const normalizedPath = path.normalize(filePath);
    if (!normalizedPath.startsWith(path.join(__dirname, path.sep))) {
        res.writeHead(403, { 'Content-Type': 'text/plain' });
        res.end('Forbidden');
        return;
    }

    // Check if file exists
    if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
        serveStaticFile(filePath, res);
    } else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found');
    }
});

// Start server
server.listen(PORT, () => {
    console.log(`\n🚀 Squad Dashboard Server`);
    console.log(`\n📍 Running at: http://localhost:${PORT}`);
    console.log(`📊 API endpoint: http://localhost:${PORT}/api/status`);
    console.log(`📁 Data file: ${DATA_FILE}`);
    console.log(`\n💡 To update data, edit: ${DATA_FILE}`);
    console.log(`\n✨ Dashboard will auto-refresh every 60 seconds`);
    console.log(`\nPress Ctrl+C to stop\n`);
});

// Handle graceful shutdown
process.on('SIGINT', () => {
    console.log('\n\n🛑 Shutting down server...');
    server.close(() => {
        console.log('✅ Server stopped');
        process.exit(0);
    });
});

process.on('SIGTERM', () => {
    console.log('\n\n🛑 Shutting down server...');
    server.close(() => {
        console.log('✅ Server stopped');
        process.exit(0);
    });
});
