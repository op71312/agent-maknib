const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const aiRoutes = require('./api/routes/routes');

const app = express();
app.use(cors());
app.use(express.json());
app.use('/', aiRoutes);

// เชื่อมต่อ MongoDB
mongoose.connect('mongodb://localhost:27017/agentmaknib', {
  useNewUrlParser: true,
  useUnifiedTopology: true
}).then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB error:', err));

const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
