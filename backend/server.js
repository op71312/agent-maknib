require('dotenv').config();
const PORT = 5000; 

const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const aiRoutes = require('./api/routes/routes');

const app = express();
app.use(cors());
app.use(express.json());
app.use('/', aiRoutes);


app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
