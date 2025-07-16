const mongoose = require('mongoose')

const MoveSchema = new mongoose.Schema({
  turn: Number,
  player: String, 
  from: String,   
  to: String,    
  timeUsed: Number 
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
}, { versionKey: false });

module.exports = mongoose.model('GameHistory', GameHistorySchema)
