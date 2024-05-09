const express = require('express');
const path = require('path');
const app = express();

app.use(express.static(__dirname));

app.get('/favicon.ico', (req, res) => {
    res.sendFile(path.join(__dirname, 'imgs/setup/favicon.ico'));
});

app.listen(8080, () => {
    console.log('Server running on http://localhost:8080');
});