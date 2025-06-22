const express = require('express');
const router = express.Router();
const controller = require('../controllers/controller');

router.post('/ai/move', controller.getAIMove);
router.get('/ai/move', (req, res) => {
   // สมมติ AI เดินจาก [0,0] ไป [0,1] ทุกครั้ง
  res.json({
    from: [0, 0],
    to: [0, 1],
    thoughts: 'AI ตัดสินใจเดินหมากจาก [1,1] ไป [1,2] เพื่อเปิดเกม'
  });
});

module.exports = router;
