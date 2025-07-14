const { dummyAI } = require('../models/model');
const { indexToPosition } = require('../utils/position');
const GameHistory = require('../models/GameHistory');

/*exports.getAIMove = (req, res) => {
  const { boardState, difficulty, timeLeft, moveHistory, aiPieceId } = req.body;

  if (!boardState || !difficulty || typeof timeLeft !== 'number') {
    return res.status(400).json({ error: 'ข้อมูลไม่ครบหรือไม่ถูกต้อง' });
  }

  const result = dummyAI(boardState, difficulty, timeLeft, aiPieceId, moveHistory);

  if (!result.from || !result.to) {
    return res.status(200).json({ error: 'ไม่สามารถหาการเดินที่เหมาะสมได้' });
  }

  return res.json({
    from: indexToPosition(...result.from),
    to: indexToPosition(...result.to),
    thoughts: result.thoughts
  });
};*/

exports.getAIMove = async (req, res) => {
  // รับข้อมูลจาก frontend
  const {
    boardState,
    difficulty,
    timeLeft,
    pieceId,         // หมายเลขประจำหมาก (array หรือ object)
    move_history     // { ai: [...], player: [...] }
  } = req.body;

  // ตรวจสอบข้อมูล
  if (!boardState || !difficulty || typeof timeLeft !== 'number' || !move_history) {
    return res.status(400).json({ error: 'ข้อมูลไม่ครบหรือไม่ถูกต้อง' });
  }

  // เตรียมข้อมูลส่งให้ LLM
  const llmPayload = {
    boardState,
    difficulty,
    timeLeft,
    pieceId,
    move_history
  };

  // ตัวอย่าง: ส่งข้อมูลไป LLM (คุณต้องเขียนฟังก์ชัน callLLM เอง)
  // const llmResult = await callLLM(llmPayload);

  // ตัวอย่างผลลัพธ์จำลอง (ให้แก้ไขตามจริง)
  res.json({
    from: [0, 0],
    to: [1, 0],
    thoughts: 'AI ตัดสินใจเดินหมากจาก [1,1] ไป [2,1] เพื่อเปิดเกม',
    llmPayload // ส่งกลับไปดูโครงสร้างข้อมูลที่ส่งให้ LLM (สำหรับ debug)
  });
};

// เรียกเมื่อจบเกม
exports.saveGameHistory = async (req, res) => {
  try {
    console.log('saveGameHistory called', req.body)
    // รับข้อมูลจาก frontend
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



