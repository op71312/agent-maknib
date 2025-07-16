const express = require('express');
const router = express.Router();
const controller = require('../controllers/controller');

router.post('/ai/move', controller.getAIMove);
router.post('/save-history', controller.saveGameHistory)

module.exports = router;
