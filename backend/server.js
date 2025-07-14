require('dotenv').config(); // เพิ่มบรรทัดนี้ไว้บนสุด (ถ้ายังไม่มี)
const PORT = process.env.PORT || 5000; // เพิ่มบรรทัดนี้ก่อน app.listen

const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const aiRoutes = require('./api/routes/routes');

const app = express();
app.use(cors());
app.use(express.json());
app.use('/', aiRoutes);

// เชื่อมต่อ MongoDB


const dbURI = process.env.DB_URI;

mongoose.Promise = global.Promise;

async function connectDB() {
  try {
    await mongoose.connect(dbURI, {
      useNewUrlParser: true,
      useUnifiedTopology: true,
    });
    console.log('Database connected successfully');
  } catch (error) {
    console.error('Database connection error:', error);
  }
}

connectDB();


app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
