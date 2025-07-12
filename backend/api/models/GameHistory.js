const mongoose = require('mongoose')

const MoveSchema = new mongoose.Schema({
  turn: Number,
  player: String, // 'X' หรือ 'O'
  from: String,   // เช่น 'a2'
  to: String,     // เช่น 'c2'
  timeUsed: Number // วินาทีที่ใช้ในแต่ละตา
}, { _id: false })

const GameHistorySchema = new mongoose.Schema({
  moves: [MoveSchema],
  winner: String,
  xMoveCount: Number,
  oMoveCount: Number,
  xScore: Number,      
  oScore: Number,     
  xTotalTime: Number,
  oTotalTime: Number,
  level: String,
  createdAt: { type: Date, default: Date.now }
})

module.exports = mongoose.model('GameHistory', GameHistorySchema)
