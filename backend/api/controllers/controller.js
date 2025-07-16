const { dummyAI } = require('../models/model');
const { indexToPosition } = require('../utils/position');
const GameHistory = require('../models/GameHistory');


exports.getAIMove = async (req, res) => {
  const {
    boardState,
    difficulty,
    timeLeft,
    pieceId,         
    move_history     
  } = req.body;

  if (!boardState || !difficulty || typeof timeLeft !== 'number' || !move_history) {
    return res.status(400).json({ error: 'ข้อมูลไม่ครบหรือไม่ถูกต้อง' });
  }

  const llmPayload = {
    boardState,
    difficulty,
    timeLeft,
    pieceId,
    move_history
  };

  res.json({
    from: [0, 0],
    to: [1, 0],
    thoughts: 'AI ตัดสินใจเดินหมากจาก [1,1] ไป [2,1] เพื่อเปิดเกม',
    llmPayload 
  });
};

exports.saveGameHistory = async (req, res) => {
  try {
    console.log('saveGameHistory called', req.body)
    const {
      moves,
      winner,
      xMoveCount,
      oMoveCount,
      xScore,
      oScore,
      xTotalTime,
      oTotalTime,
      level
    } = req.body

    const history = new GameHistory({
      moves,
      winner,
      xMoveCount,
      oMoveCount,
      xScore,
      oScore,
      xTotalTime,
      oTotalTime,
      level
    })

    await history.save()
    res.status(201).json({ message: 'Saved', id: history._id })
  } catch (err) {
    res.status(500).json({ error: err.message })
  }
}



