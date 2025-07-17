const { dummyAI } = require('../models/model');
const { indexToPosition } = require('../utils/position');


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
    llmPayload 
  });
};



