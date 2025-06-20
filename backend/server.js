const express = require('express');
const cors = require('cors');
const aiRoutes = require('./api/routes/routes');

const app = express();
app.use(cors());
app.use(express.json());
app.use('/', aiRoutes);

const PORT = 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
