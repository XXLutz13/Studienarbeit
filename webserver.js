// express und http Module importieren. Sie sind dazu da, die HTML-Dateien
// aus dem Ordner "public" zu veröffentlichen.
// var express = require('express');
// var app = express();
// var server = require('http').createServer(app);
// var port = 3000;

const express = require("express");
const http = require("http");
const WebSocket = require("ws"); 

const app = express();
const webServer = http.createServer(app);
const webSocketServer = new WebSocket.Server({ server: webServer });

// use public files in the dir: '/Website'
app.use(express.static(__dirname + '/Website'));

// starts the Webserver on 3000
app.listen(3000, () => {
    console.log("server started on http://localhost:3000");
});

// starts the Websocket on 3001
webServer.listen(3001, () => {
    console.log(`WebSocket started on http://localhost:3001`);
});

