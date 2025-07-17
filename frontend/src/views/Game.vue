<template>
  <div class="game-container">
    <div class="fire-background"></div>
    <div class="ambient-particles"></div>
    <div class="content">
      <div v-if="!isPvP" class="ai-thoughts-panel">
        <div class="panel-header">
          <div class="ai-icon">🤖</div>
          <h3 class="panel-title">AI's Analysis</h3>
        </div>
        <div class="thoughts-history">
          <div v-for="(entry, index) in aiThoughtHistory"
               :key="index"
               class="thought-entry"
               :class="{ 'latest': index === 0 }">
            <div class="thought-header">
              <span class="turn-number">Turn {{entry.turn}}</span>
              <span class="timestamp">{{entry.timestamp}}</span>
            </div>
            <div class="thought-content">
              {{entry.thoughts}}
            </div>
          </div>
          <div v-if="aiThoughtHistory.length === 0" class="empty-thoughts">
            <div class="thinking-animation">
              <div class="dot"></div>
              <div class="dot"></div>
              <div class="dot"></div>
            </div>
            <p>Waiting for AI analysis...</p>
          </div>
        </div>
      </div>

      <div class="game-content" :class="{ 'full-width': isPvP }">
        <div class="game-header">
          <h2 class="difficulty-display">
            <span class="difficulty-icon">⚔️</span>
            ระดับ: {{ difficultyText }}
          </h2>
          
          <div class="game-info">
            <div class="game-status-bar">
              <div class="info-card timer-card" :aria-label="'เวลาที่เหลือ: ' + Math.floor(timeLeft / 60) + ' นาที ' + (timeLeft % 60) + ' วินาที'">
                <div class="info-icon">⏳</div>
                <div class="info-content">
                  <div class="info-label">เวลา</div>
                  <div class="info-value" :class="{ 'warning': timeLeft < 60, 'critical': timeLeft < 30 }">
                    {{ Math.floor(timeLeft / 60) }}:{{ (timeLeft % 60).toString().padStart(2, '0') }}
                  </div>
                </div>
              </div>
              
              <div class="info-card turn-card">
                <div class="info-icon">👤</div>
                <div class="info-content">
                  <div class="info-label">ถึงตา</div>
                  <div class="info-value player-name" :class="{ 'player-x': currentPlayer === 'X', 'player-o': currentPlayer === 'O' }">
                    {{ currentPlayer === 'X' ? 'ผู้เล่น ⚫' : (isPvP ? 'ผู้เล่น 🔴' : 'AI 🔴') }}
                  </div>
                </div>
              </div>
              
              <div class="info-card score-card">
                <div class="info-content">
                  <div class="info-label">คะแนน</div>
                  <div class="score-inline">
                    <span class="score-x">⚫ {{ xScore }}</span>
                    <span class="vs-divider">VS</span>
                    <span class="score-o">🔴 {{ oScore }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="game-board-container">
          <div class="board-wrapper">
            <div class="board" role="grid" aria-label="กระดานเกม">
              <div class="board-glow"></div>
              <div 
                v-for="(row, rowIndex) in board"
                :key="rowIndex"
                class="row"
                role="row"
              >
                <div
                  v-for="(cell, colIndex) in row" 
                  :key="colIndex"
                  class="cell"
                  :class="{
                    'cell-light': (rowIndex + colIndex) % 2 === 0,
                    'cell-dark': (rowIndex + colIndex) % 2 === 1,
                    'selected': isSelected(rowIndex, colIndex),
                    'possible-move': isPossibleMove(rowIndex, colIndex),
                    'has-piece': cell !== ''
                  }"
                  @click="handleClick(rowIndex, colIndex)"
                  role="gridcell"
                  :aria-selected="isSelected(rowIndex, colIndex)"
                  tabindex="0"
                  @keydown.enter.prevent="handleClick(rowIndex, colIndex)"
                >
                  <div v-if="cell"
                       class="piece"
                       :class="getPieceClasses(cell)"
                       :aria-label="cell === 'X' ? 'หมากสีดำ' : 'หมากสีแดง'">
                    <div class="piece-inner"></div>
                    <div class="piece-shine"></div>
                  </div>
                  <div v-if="isPossibleMove(rowIndex, colIndex)" class="move-indicator">
                    <div class="move-dot"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <button class="control-button back-btn" @click="goBack" aria-label="กลับสู่เมนูระดับ">
            <i class="icon">🏠</i>
            <span>กลับ</span>
          </button>
        </div>

        <div v-if="isGameOver" class="game-over-overlay">
          <div class="game-over-panel">
            <div class="game-over-icon">
              <div v-if="!isPvP && winner === 'O'" class="loser-icon">💔</div>
              <div v-else-if="!isPvP && winner === 'X'" class="winner-icon">🏆</div>
              <div v-else-if="winner === 'draw'" class="draw-icon">🤝</div>
              <div v-else class="winner-icon">🏆</div>
            </div>
            
            <h2 class="game-over-title">จบเกม</h2>
            
            <div class="game-result">
              <p v-if="!isPvP && winner === 'O'" class="result-text loser">
                คุณแพ้ AI 😢
              </p>
              <p v-else-if="!isPvP && winner === 'X'" class="result-text winner">
                คุณชนะ AI! 🎉
              </p>
              <p v-else-if="winner === 'draw'" class="result-text draw">
                เสมอ!
              </p>
              <p v-else class="result-text winner">
                ผู้ชนะ: {{ winner === 'X' ? 'ผู้เล่น ⚫' : 'ผู้เล่น 🔴' }}
              </p>
            </div>

            <div class="final-scores">
              <div class="final-score">
                <span class="final-score-label">{{ !isPvP ? 'คุณ (⚫)' : 'ผู้เล่น ⚫' }}:</span>
                <span class="final-score-value">{{ xScore }}</span>
              </div>
              <div class="final-score">
                <span class="final-score-label">{{ !isPvP ? 'AI (🔴)' : 'ผู้เล่น 🔴' }}:</span>
                <span class="final-score-value">{{ oScore }}</span>
              </div>
            </div>

            <div class="game-over-buttons">
              <button class="control-button back-btn" @click="goBack">
                <i class="icon">🏠</i>
                <span>กลับหน้าหลัก</span>
              </button>
              <button class="control-button replay-btn" @click="restartGame">
                <i class="icon">🔄</i>
                <span>เล่นอีกครั้ง</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const size = ref(8)
const timeLeft = ref(900) 
const currentPlayer = ref('X')
const selected = ref(null)
const aiThoughts = ref('') 
const aiThoughtHistory = ref([])
const moveHistory = ref([]) 

const difficulty = defineProps({
  difficulty: {
    type: String,
    required: true,
    validator: (val) => ['easy', 'medium', 'hard', 'friend'].includes(val)
  }
})

const difficultyText = computed(() => {
  const map = { easy: 'ง่าย', medium: 'กลาง', hard: 'ยาก', friend: 'เล่นกับเพื่อน' }
  return map[difficulty.difficulty]
})

const isPvP = computed(() => difficulty.difficulty === 'friend')

const board = ref([
  ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
  ...Array(6).fill().map(() => Array(size.value).fill('')),
  ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
])

const xScore = ref(0)
const oScore = ref(0)
const isGameOver = ref(false)
const winner = ref('')
const xTotalTime = ref(0)
const oTotalTime = ref(0) 
const turnStartTime = ref(timeLeft.value)

function getBoardState() {
  return board.value.map(row =>
    row.map(cell => (cell === 'O' ? -1 : cell === 'X' ? 1 : 0))
  )
}

function isSelected(row, col) {
  return selected.value?.[0] === row && selected.value?.[1] === col
}

function isStraightMove(r1, c1, r2, c2) {
  const sameRow = r1 === r2 && c1 !== c2;
  const sameCol = c1 === c2 && r1 !== r2;
  return sameRow || sameCol;
}

function isPathClear(r1, c1, r2, c2) {
  if (r1 === r2) {
    const start = Math.min(c1, c2) + 1;
    const end = Math.max(c1, c2);
    for (let c = start + 1; c < end; c++) {
      if (board.value[r1][c] !== '') return false;
    }
  } else if (c1 === c2) {
    const start = Math.min(r1, r2) + 1;
    const end = Math.max(r1, r2);
    for (let r = start + 1; r < end; r++) {
      if (board.value[r][c1] !== '') return false;
    }
  } else {
    return false;
  }
  return true;
}

function handleClick(row, col) {
  if (!isPvP.value && currentPlayer.value !== 'X') return
  
  const piece = board.value[row][col]
  
  if (selected.value) {
    const [fromRow, fromCol] = selected.value
    if (
      board.value[row][col] === '' &&
      isStraightMove(fromRow, fromCol, row, col) &&
      isPathClear(fromRow, fromCol, row, col)
    ) {
      board.value[row][col] = board.value[fromRow][fromCol]
      board.value[fromRow][fromCol] = ''
      selected.value = null
      checkCapture(row, col)
      
      const timeUsedSec = turnStartTime.value - timeLeft.value
      moveHistory.value.push({
        turn: moveHistory.value.length + 1,
        player: currentPlayer.value,
        from: toChessPos(fromRow, fromCol),
        to: toChessPos(row, col),
        timeUsed: timeUsedSec 
      })
      
      if (currentPlayer.value === 'X') {
        xTotalTime.value += timeUsedSec
      } else {
        oTotalTime.value += timeUsedSec
      }
      
      switchPlayer()
      analyzeStrategyIfNeeded()
    } else {
      selected.value = null
    }
  } else if (piece === currentPlayer.value) {
    selected.value = [row, col]
  }
}

function inBounds(row, col) {
  return row >= 0 && col >= 0 && row < size.value && col < size.value
}

function checkCapture(row, col) {
  const dirs = [
    [0, 1], [1, 0], [0, -1], [-1, 0]
  ];
  const enemy = currentPlayer.value === 'X' ? 'O' : 'X';
  let capturedSet = new Set();

  for (const [dr, dc] of dirs) {
    let toCapture = [];
    let r = row + dr, c = col + dc;
    while (inBounds(r, c) && board.value[r][c] === enemy) {
      toCapture.push([r, c]);
      r += dr; c += dc;
    }
    if (toCapture.length > 0 && inBounds(r, c) && board.value[r][c] === currentPlayer.value) {
      for (const [cr, cc] of toCapture) {
        capturedSet.add(`${cr},${cc}`);
      }
    }

    const adj1 = [row - dr, col - dc];
    const adj2 = [row + dr, col + dc];
    if (
      inBounds(adj1[0], adj1[1]) && inBounds(adj2[0], adj2[1]) &&
      board.value[adj1[0]][adj1[1]] === enemy &&
      board.value[adj2[0]][adj2[1]] === enemy
    ) {
      capturedSet.add(`${adj1[0]},${adj1[1]}`);
      capturedSet.add(`${adj2[0]},${adj2[1]}`);
    }
  }

  let captured = 0;
  for (const pos of capturedSet) {
    const [r, c] = pos.split(',').map(Number);
    board.value[r][c] = '';
    captured++;
  }

  if (captured > 0) {
    if (currentPlayer.value === 'X') xScore.value += captured;
    else oScore.value += captured;
    checkGameEnd();
  }
}

function switchPlayer() {
  currentPlayer.value = currentPlayer.value === 'X' ? 'O' : 'X'
  turnStartTime.value = timeLeft.value 
  if (!isPvP.value && currentPlayer.value === 'O') {
    requestAIMove()
  }
}

async function requestAIMove() {
  try {
    const response = await axios.post('http://localhost:8000/ai-move', {
      board: getBoardState(),
      current_player: -1 
    })
    const { from_row, from_col, to_row, to_col, action_id } = response.data
    board.value[to_row][to_col] = board.value[from_row][from_col]
    board.value[from_row][from_col] = ''
    checkCapture(to_row, to_col)
    aiThoughtHistory.value.unshift({
      turn: aiThoughtHistory.value.length + 1,
      thoughts: `AI เลือกเดินจาก (${from_row},${from_col}) ไป (${to_row},${to_col}) [action_id: ${action_id}]`,
      timestamp: new Date().toLocaleTimeString()
    })
  } catch (err) {
    console.error('AI move error:', err)
  } finally {
    currentPlayer.value = 'X'
  }
}

async function saveGameHistory() {

  try {
    await axios.post('http://localhost:5000/save-history', {
      moves: moveHistory.value,
      winner: winner.value,
      xMoveCount: moveHistory.value.filter(m => m.player === 'X').length,
      oMoveCount: moveHistory.value.filter(m => m.player === 'O').length,
      xScore: xScore.value,
      oScore: oScore.value,
      xTotalTime: xTotalTime.value,
      oTotalTime: oTotalTime.value,
      level: difficulty.difficulty
    })
  } catch (err) {
    console.error('Save history error:', err)
  }
}

function goBack() {
  router.push('/level')
}

function isPossibleMove(row, col) {
  if (!selected.value || board.value[row][col] !== '') return false
  
  const [selectedRow, selectedCol] = selected.value
  const currentPiece = board.value[selectedRow][selectedCol]
  
  if (currentPiece !== currentPlayer.value) return false
  
  const isHorizontal = selectedRow === row && selectedCol !== col
  const isVertical = selectedCol === col && selectedRow !== row
  
  if (isHorizontal) {
    const start = Math.min(selectedCol, col)
    const end = Math.max(selectedCol, col)
    for (let c = start + 1; c < end; c++) {
      if (board.value[row][c] !== '') return false
    }
    return true
  }
  
  if (isVertical) {
    const start = Math.min(selectedRow, row)
    const end = Math.max(selectedRow, row)
    for (let r = start + 1; r < end; r++) {
      if (board.value[r][col] !== '') return false
    }
    return true
  }
  
  return false
}

function getPieceClasses(cell) {
  return {
    'piece-black': cell === 'X',
    'piece-red': cell === 'O'
  }
}

function checkGameEnd() {
  if (xScore.value >= 8) {
    isGameOver.value = true
    winner.value = 'X'
    saveGameHistory()
  } else if (oScore.value >= 8) {
    isGameOver.value = true
    winner.value = 'O'
    saveGameHistory()
  } else if (timeLeft.value <= 0) {
    isGameOver.value = true
    if (xScore.value > oScore.value) winner.value = 'X'
    else if (oScore.value > xScore.value) winner.value = 'O'
    else winner.value = 'draw'
    saveGameHistory()
  }
}

function toChessPos(row, col) {
  const file = String.fromCharCode('a'.charCodeAt(0) + col)
  const rank = 8 - row
  return file + rank
}

function formatTimeUsed(seconds) {
  const min = Math.floor(seconds / 60)
  const sec = seconds % 60
  if (min > 0) {
    return `${min} min ${sec} sec`
  } else {
    return `${sec} sec`
  }
}

const timerInterval = ref(null)

const startTimer = () => {
  timerInterval.value = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
      if (timeLeft.value === 0) checkGameEnd()
    }
  }, 1000)
}


startTimer()

onUnmounted(() => {
  clearInterval(timerInterval.value)
})

function restartGame() {
  board.value = [
    ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O'],
    ...Array(6).fill().map(() => Array(size.value).fill('')),
    ['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
  ]
  xScore.value = 0
  oScore.value = 0
  currentPlayer.value = 'X'
  selected.value = null
  isGameOver.value = false
  winner.value = ''
  timeLeft.value = 900
  aiThoughtHistory.value = []
  moveHistory.value = []
  turnStartTime.value = timeLeft.value
}

async function analyzeStrategyIfNeeded() {
  if (moveHistory.value.length > 0 && moveHistory.value.length % 10 === 0) {
    // สร้าง string ประวัติการเดิน
    const movesText = moveHistory.value.map((m, idx) => {
      const player = m.player === 'X' ? 'P1' : 'P2'
      // สมมติ m.from_row, m.from_col, m.to_row, m.to_col มีอยู่
      return `[${idx + 1}] ${player}: (${m.from_row},${m.from_col})→(${m.to_row},${m.to_col})`
    }).join('\n')

    try {
      const res = await axios.post('http://localhost:8000/analyze-strategy', {
        move_history: movesText
      })
      aiThoughtHistory.value.unshift({
        turn: moveHistory.value.length,
        thoughts: res.data.analysis,
        timestamp: new Date().toLocaleTimeString()
      })
    } catch (err) {
      console.error('AI strategy analysis error:', err)
    }
  }
}
</script>

<style scoped>
.game-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: radial-gradient(ellipse at center, #1a0000 0%, #000000 70%);
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  box-sizing: border-box;
}

.fire-background,
.ambient-particles {
  position: fixed; 
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  transform: translateZ(0);
}

.content {
  position: relative;
  z-index: 1;
  width: 100%; 
  flex-grow: 1; 
  display: grid; 
  grid-template-columns: 350px 1fr;
  gap: 2rem;
  padding: 2rem; 
  transform: translateZ(0);
  min-height: calc(100vh - 4rem); 
}

.ai-thoughts-panel {
  height: 100%; 
  background: linear-gradient(145deg,  rgba(97, 26, 26, 0.95), rgba(10, 0, 0, 0.98)); 
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 
    0 10px 20px rgba(255, 0, 0, 0.15), 
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 69, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden; 
  transform: translateZ(0); 
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 69, 0, 0.2);
}

.ai-icon {
  font-size: 2rem;
  animation: pulse 2s ease-in-out infinite;
}

.panel-title {
  color: #e8eaed;
  font-size: 1.4rem;
  font-weight: 600;
  margin: 0;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.thoughts-history {
  flex: 1;
  overflow-y: auto; 
  padding-right: 0.5rem;
}

.thought-entry {
  background: linear-gradient(135deg, rgba(255, 69, 0, 0.08), rgba(139, 0, 0, 0.05));
  border-radius: 12px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  border: 1px solid rgba(255, 69, 0, 0.15);
  transition: all 0.3s ease;
}

.thought-entry.latest {
  border-color: rgba(255, 215, 0, 0.4);
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.15);
}

.thought-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  color: #ffb74d;
  font-size: 0.85rem;
}

.turn-number {
  font-weight: 600;
  color: #ffd700;
}

.timestamp {
  opacity: 0.7;
}

.thought-content {
  color: #e8eaed;
  line-height: 1.5;
  font-size: 0.9rem;
}

.empty-thoughts {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #ff8a65;
  text-align: center;
}

.thinking-animation {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.dot {
  width: 8px;
  height: 8px;
  background: #ff8a65;
  border-radius: 50%;
  animation: thinking 1.4s ease-in-out infinite both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

.game-content {
  height: 100%; 
  background: linear-gradient(145deg, rgba(97, 26, 26, 0.95), rgba(10, 0, 0, 0.98)); 
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 
    0 10px 20px rgba(186, 41, 41, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 69, 0, 0.13);
  display: flex;
  flex-direction: column;
  overflow: hidden; 
  transform: translateZ(0); 
}

.game-content.full-width {
  grid-column: 1 / -1; 
}

.game-header {
  margin-bottom: 2rem;
}

.difficulty-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: #ff6b6b;
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 2rem;
  text-shadow: 
    0 0 10px rgba(255, 69, 0, 0.8),
    0 0 20px rgba(255, 69, 0, 0.6);
  letter-spacing: 1px;
}

.difficulty-icon {
  font-size: 2.5rem;
  animation: bounce 2s ease-in-out infinite;
}

.game-info {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: stretch;
}

.game-status-bar {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 1.5rem;
}

.info-card {
  flex: 1 1 0;
  min-width: 0;
  max-width: none;
  background: linear-gradient(135deg, rgba(255, 69, 0, 0.15), rgba(139, 0, 0, 0.1));
  border-radius: 16px;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.7rem;
  border: 1px solid rgba(255, 69, 0, 0.2);
  box-sizing: border-box;
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(255, 69, 0, 0.2);
}

.info-card .info-content {
  width: 100%;
  text-align: center;
}

.info-icon {
  font-size: 2rem;
  opacity: 0.9;
}

.info-content {
  flex: 1;
}

.info-label {
  color: #ffb74d;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.info-value {
  color: #fff;
  font-size: 1.3rem;
  font-weight: 600;
  transition: color 0.3s ease;
}

.info-value.warning {
  color: #ffb74d;
  animation: pulse 1s ease-in-out infinite;
}

.info-value.critical {
  color: #f44336;
  animation: pulse 0.5s ease-in-out infinite;
}

.player-name.player-x {
  color: #fff176;
}

.player-name.player-o {
  color: #ef5350;
}

.score-inline {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.7rem;
  font-size: 1.2rem;
  color: #fff;
}

.vs-divider {
  color: #ff6b6b;
  font-size: 1rem;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
}

.game-board-container {
  position: relative;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  min-height: 0; 
  overflow-y: auto; 
}

.board-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  max-width: 600px;
}

.board {
  position: relative;
  display: grid;
  grid-template-rows: repeat(8, 1fr);
  gap: 3px;
  background: linear-gradient(145deg, #2c1810, #1a0f08);
  padding: 20px;
  border-radius: 20px;
  border: 3px solid rgba(255, 69, 0, 0.3);
  box-shadow: 
    0 0 40px rgba(255, 69, 0, 0.2),
    inset 0 0 20px rgba(0, 0, 0, 0.5);
  user-select: none;
  width: 100%;
  aspect-ratio: 1;
}

.board-glow {
  position: absolute;
  top: -6px;
  left: -6px;
  right: -6px;
  bottom: -6px;
  border-radius: 24px;
  background: linear-gradient(45deg, 
    rgba(255, 69, 0, 0.4), 
    rgba(255, 140, 0, 0.3), 
    rgba(255, 69, 0, 0.4));
  background-size: 200% 200%;
  animation: boardGlow 4s ease-in-out infinite;
  z-index: -1;
  filter: blur(4px); 
  transform: translateZ(0); 
}

.row {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 3px;
}

.cell {
  aspect-ratio: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  outline-offset: 4px;
  overflow: hidden;
  min-width: 0;
}

.cell::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.cell:hover::before {
  opacity: 1;
}

.cell-coordinates {
  position: absolute;
  top: 2px;
  left: 4px;
  font-size: 0.6rem;
  color: rgba(255, 255, 255, 0.4);
  font-weight: 500;
  pointer-events: none;
}

.cell:hover:not(.selected):not(.has-piece) {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.4);
}

.cell:focus-visible {
  outline: 3px solid #ffd700;
  outline-offset: 3px;
  z-index: 10;
}

.cell-light {
  background: linear-gradient(145deg, #f5deb3, #deb887);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cell-dark {
  background: linear-gradient(145deg, #8b4513, #654321);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.2);
}

.piece {
  width: 85%;
  height: 85%;
  border-radius: 50%;
  position: relative;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  overflow: hidden;
}

.piece-inner {
  position: absolute;
  top: 20%;
  left: 20%;
  right: 20%;
  bottom: 20%;
  border-radius: 50%;
  background: inherit;
  filter: brightness(1.3);
}

.piece-shine {
  position: absolute;
  top: 25%;
  left: 30%;
  width: 25%;
  height: 25%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.6), transparent);
  border-radius: 50%;
  filter: blur(1px);
}

.piece-black {
  background: linear-gradient(145deg, #2c3e50, #1a252f);
  border: 2px solid #34495e;
  box-shadow: 
    0 4px 8px rgba(0, 0, 0, 0.4),
    inset 0 2px 4px rgba(255, 255, 255, 0.1);
}

.piece-red {
  background: linear-gradient(145deg, #e74c3c, #c0392b);
  border: 2px solid #e67e22;
  box-shadow: 
    0 4px 8px rgba(231, 76, 60, 0.4),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.selected {
  box-shadow: 
    inset 0 0 20px rgba(255, 215, 0, 0.7),
    0 0 30px rgba(255, 215, 0, 0.5);
  transform: scale(1.1);
  z-index: 5;
}

.selected .piece {
  transform: scale(1.1);
  box-shadow: 
    0 0 25px rgba(255, 215, 0, 0.7),
    0 4px 8px rgba(0, 0, 0, 0.3);
}

.possible-move {
  box-shadow: inset 0 0 15px rgba(76, 175, 80, 0.7);
  animation: possibleMove 1.5s ease-in-out infinite;
}

.move-indicator {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  pointer-events: none;
}

.move-dot {
  width: 12px;
  height: 12px;
  background: #4caf50;
  border-radius: 50%;
  box-shadow: 0 0 10px rgba(76, 175, 80, 0.8);
  animation: moveDot 1s ease-in-out infinite;
}

.game-controls {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.control-button {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: linear-gradient(135deg, #dc143c, #8b0000);
  border: none;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  padding: 1rem 2rem;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(220, 20, 60, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Kanit', sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.control-button:hover {
  background: linear-gradient(135deg, #ff1744, #dc143c);
  box-shadow: 0 8px 25px rgba(220, 20, 60, 0.4);
  transform: translateY(-3px);
}

.control-button:active {
  transform: translateY(-1px);
}

.control-button .icon {
  font-size: 1.2rem;
}

.back-btn {
  position: absolute;
  bottom: 0.5rem; 
  right: 0.5rem; 
  background: linear-gradient(135deg, #ff6b6b, #dc143c);
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 1.5rem 0.1rem;
  border-radius: 50px; 
  box-shadow: 0 4px 15px rgba(220, 20, 60, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}

.back-btn:hover {
  background: linear-gradient(135deg, #ff1744, #dc143c);
  box-shadow: 0 8px 25px rgba(220, 20, 60, 0.4);
  transform: translateY(-3px);
}

.back-btn:active {
  transform: translateY(-1px);
}

.back-btn .icon {
  font-size: 1.2rem;
}

.game-over-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
  transform: translateZ(0); 
}

.game-over-panel {
  background: linear-gradient(145deg, rgba(30, 0, 0, 0.95), rgba(10, 0, 0, 0.98)); 
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 
    0 10px 20px rgba(255, 0, 0, 0.25), 
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 69, 0, 0.3);
  text-align: center;
  min-width: 400px;
  animation: slideUp 0.4s ease;
  transform: translateZ(0); 
}

.game-over-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: bounce 1s ease-in-out infinite;
}

.game-over-title {
  color: #ff6b6b;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
}

.game-result {
  margin-bottom: 2rem;
}

.result-text {
  font-size: 1.5rem;
  margin: 0;
}

.result-text.draw {
  color: #ffb74d;
}

.result-text.winner {
  color: #4caf50;
}

.result-text.loser {
  color: #ff6b6b;  
  text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);  
  font-weight: bold; 
}

.winner-name {
  font-weight: 700;
  font-size: 1.8rem;
}

.winner-name.winner-x {
  color: #fff176;
  text-shadow: 0 0 10px rgba(255, 241, 118, 0.5);
}

.winner-name.winner-o {
  color: #ef5350;
  text-shadow: 0 0 10px rgba(239, 83, 80, 0.5);
}

.final-scores {
  display: flex;
  justify-content: space-around;
  margin-bottom: 2rem;
  padding: 1rem;
  background: rgba(255, 69, 0, 0.1);
  border-radius: 12px;
}

.final-score {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.final-score-label {
  color: #ffb74d;
  font-size: 0.9rem;
}

.final-score-value {
  color: #fff;
  font-size: 1.5rem;
  font-weight: 700;
}

.game-over-buttons {
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 2rem;
}

.back-btn, .replay-btn {
  min-width: 160px;
  justify-content: center;
}

.back-btn {
  background: linear-gradient(135deg, #dc143c, #8b0000);
}

.replay-btn {
  background: linear-gradient(135deg, #4caf50, #2e7d32);
}

@media (max-width: 480px) {
  .game-over-buttons {
    flex-direction: column;
  }
  
  .back-btn, .replay-btn {
    width: 100%;
  }
}

.thoughts-history::-webkit-scrollbar {
  width: 6px;
}

.thoughts-history::-webkit-scrollbar-track {
  background: rgba(255, 69, 0, 0.1);
  border-radius: 3px;
}

.thoughts-history::-webkit-scrollbar-thumb {
  background: rgba(255, 69, 0, 0.3);
  border-radius: 3px;
}

.thoughts-history::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 69, 0, 0.5);
}

@keyframes fireEffect1 {
  0%, 100% { background-position: 0% 50%, 0% 50%, 0% 50%, 0% 50%; }
  50% { background-position: 100% 50%, 100% 50%, 100% 50%, 100% 50%; }
}

@keyframes fireEffect2 {
  0%, 100% { background-position: 100% 0%, 0% 100%, 50% 50%, 25% 75%; }
  50% { background-position: 0% 100%, 100% 0%, 75% 25%, 75% 25%; }
}

@keyframes fireEffect3 {
  0%, 100% { background-position: 50% 0%, 50% 100%, 0% 50%, 100% 50%; }
  50% { background-position: 0% 100%, 100% 0%, 100% 50%, 0% 50%; }
}

@keyframes sparkle {
  0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.6; }
  50% { transform: translateY(-10px) rotate(180deg); opacity: 1; }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-8px); }
  60% { transform: translateY(-4px); }
}

@keyframes thinking {
  0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

@keyframes boardGlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes possibleMove {
  0%, 100% { box-shadow: inset 0 0 15px rgba(76, 175, 80, 0.7); }
  50% { box-shadow: inset 0 0 25px rgba(76, 175, 80, 0.9); }
}

@keyframes moveDot {
  0%, 100% { transform: scale(1); opacity: 0.8; }
  50% { transform: scale(1.2); opacity: 1; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideUp {
  from { transform: translateY(50px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@media (max-width: 1400px) {
  .content {
    grid-template-columns: 320px 1fr;
  }
}

@media (max-width: 1200px) {
  .content {
    grid-template-columns: 1fr; 
    display: flex; 
    flex-direction: column;
    gap: 1.5rem; 
    padding-top: 2rem; 
    height: auto; 
    min-height: auto; 
    overflow-y: auto; 
  }
  
  .ai-thoughts-panel,
  .game-content {
    flex-shrink: 0; 
    flex-grow: 1; 
    min-height: 0; 
    height: auto; 
  }

  
  .game-content {
    overflow-y: auto; 
  }
}

@media (max-width: 768px) {
  .content {
    padding: 1rem; 
    gap: 1rem;
    padding-top: 1rem; 
  }
  
  .game-content {
    padding: 1.5rem;
  }
  
  .board {
    padding: 15px;
  }
  
  .board-wrapper {
    max-width: 400px;
  }
  
  .game-status-bar {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  
  .info-card {
    min-width: 0;
    width: 100%;
    max-width: 300px;
  }
  
  .difficulty-display {
    font-size: 1.5rem;
  }
  
  .game-over-panel {
    margin: 1rem;
    padding: 2rem;
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .game-content {
    padding: 1rem;
  }
  
  .board {
    padding: 10px;
  }
  
  .board-wrapper {
    max-width: 320px;
  }
  
  .difficulty-display {
    font-size: 1.3rem;
  }
  
  .info-card {
    padding: 1rem;
  }
  
  .control-button {
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
  }
  
  .cell-coordinates {
    font-size: 0.5rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .fire-background,
  .ambient-particles,
  .difficulty-icon,
  .ai-icon,
  .thinking-animation,
  .board-glow,
  .possible-move,
  .move-dot {
    animation: none;
  }
  
  .cell,
  .piece,
  .control-button {
    transition: none;
  }
}

.control-button:focus {
  outline: 3px solid rgba(255, 215, 0, 0.6);
  outline-offset: 2px;
}
</style>
