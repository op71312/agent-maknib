<template>
  <div class="game-container">
    <div class="fire-background"></div>
    <div class="ambient-particles"></div>
    <div class="content">
      <!-- AI Thoughts Panel -->
      <div class="ai-thoughts-panel">
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

      <!-- Game Content -->
      <div class="game-content">
        <div class="game-header">
          <h2 class="difficulty-display">
            <span class="difficulty-icon">⚔️</span>
            ระดับ: {{ difficultyText }}
          </h2>
          
          <div class="game-info">
            <!-- Game Status Bar -->
            <div class="game-status-bar">
              <!-- เวลา -->
              <div class="info-card timer-card" :aria-label="'เวลาที่เหลือ: ' + Math.floor(timeLeft / 60) + ' นาที ' + (timeLeft % 60) + ' วินาที'">
                <div class="info-icon">⏳</div>
                <div class="info-content">
                  <div class="info-label">เวลา</div>
                  <div class="info-value" :class="{ 'warning': timeLeft < 60, 'critical': timeLeft < 30 }">
                    {{ Math.floor(timeLeft / 60) }}:{{ (timeLeft % 60).toString().padStart(2, '0') }}
                  </div>
                </div>
              </div>
              
              <!-- ถึงตา -->
              <div class="info-card turn-card">
                <div class="info-icon">👤</div>
                <div class="info-content">
                  <div class="info-label">ถึงตา</div>
                  <div class="info-value player-name" :class="{ 'player-x': currentPlayer === 'X', 'player-o': currentPlayer === 'O' }">
                    {{ currentPlayer === 'X' ? 'ผู้เล่น   ⚫' : (isPvP ? 'ผู้เล่น   🔴' : 'AI (O)  🔴') }}
                  </div>
                </div>
              </div>
              
              <!-- คะแนน -->
              <div class="info-card score-card">
                <div class="info-content">
                  <div class="info-label">คะแนน</div>
                  <div class="score-inline">
                    <span class="score-x">⚫ Player <br>{{ xScore }}</span>
                    <span class="vs-divider">VS</span>
                    <span class="score-o">🔴 Player <br>{{ oScore }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="game-board-container">
          <div class="board" role="grid" aria-label="กระดานเกม">
            <div class="board-border"></div>
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
                  'cell-black': (rowIndex + colIndex) % 2 === 1,
                  'cell-red': (rowIndex + colIndex) % 2 === 0,
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

          <div class="game-controls">
            <button class="control-button back-button" @click="goBack" aria-label="กลับสู่เมนูระดับ">
              <i class="icon">🏠</i>
              <span>กลับ</span>
            </button>
          </div>
        </div>

        <!-- Game Over Panel -->
        <div v-if="isGameOver" class="game-over-overlay">
          <div class="game-over-panel">
            <div class="game-over-icon">
              <div v-if="winner === 'draw'" class="draw-icon">🤝</div>
              <div v-else class="winner-icon">🏆</div>
            </div>
            <h2 class="game-over-title">จบเกม</h2>
            <div class="game-result">
              <p v-if="winner === 'draw'" class="result-text draw">เสมอ!</p>
              <p v-else class="result-text winner">
                ผู้ชนะ: <span class="winner-name" :class="{ 'winner-x': winner === 'X', 'winner-o': winner === 'O' }">{{ winner }}</span>
              </p>
            </div>
            <div class="final-scores">
              <div class="final-score">
                <span class="final-score-label">Player X:</span>
                <span class="final-score-value">{{ xScore }}</span>
              </div>
              <div class="final-score">
                <span class="final-score-label">{{ isPvP ? 'Player O' : 'AI (O)' }}:</span>
                <span class="final-score-value">{{ oScore }}</span>
              </div>
            </div>
            <button class="control-button game-over-button" @click="goBack">
              <i class="icon">🏠</i>
              <span>กลับเมนู</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const size = ref(8)
const timeLeft = ref(900) // เปลี่ยนจาก 300 เป็น 900 วินาที (15 นาที)
const currentPlayer = ref('X')
const selected = ref(null)
const aiThoughts = ref('') // เพิ่มการเก็บความคิด AI
const aiThoughtHistory = ref([])
const moveHistory = ref([]) // ประวัติการเดินหมาก

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
const oTotalTime = ref(0) // ทุกครั้งที่จบตา ให้บวกเวลาที่ใช้ในตานั้นให้ฝั่งที่เดิน
const turnStartTime = ref(timeLeft.value)

function getBoardState() {
  return board.value.map(row =>
    row.map(cell => (cell === 'O' ? 1 : cell === 'X' ? -1 : 0))
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
    for (let c = start; c < end; c++) {
      if (board.value[r1][c] !== '') return false;
    }
  } else if (c1 === c2) {
    const start = Math.min(r1, r2) + 1;
    const end = Math.max(r1, r2);
    for (let r = start; r < end; r++) {
      if (board.value[r][c1] !== '') return false;
    }
  } else {
    return false;
  }
  return true;
}

function handleClick(row, col) {
  // ถ้าเป็น PvP ให้ทั้ง X และ O เล่นได้
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
      
      // บันทึกการเดินลงในประวัติ
      const timeUsedSec = turnStartTime.value - timeLeft.value
      moveHistory.value.push({
        turn: moveHistory.value.length + 1,
        player: currentPlayer.value,
        from: toChessPos(fromRow, fromCol),
        to: toChessPos(row, col),
        timeUsed: timeUsedSec // หรือ formatTimeUsed(timeUsedSec) ถ้าต้องการ string
      })
      
      // สะสมเวลาที่ใช้
      if (currentPlayer.value === 'X') {
        xTotalTime.value += timeUsedSec
      } else {
        oTotalTime.value += timeUsedSec
      }
      
      switchPlayer()
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
    [0, 1],  // ขวา
    [1, 0],  // ล่าง
    [0, -1], // ซ้าย
    [-1, 0], // บน
  ]
  
  const enemy = currentPlayer.value === 'X' ? 'O' : 'X'
  let captured = 0
  
  for (const [dr, dc] of dirs) {
    // --- รูปแบบที่ 1: เดินเข้าไปตรงกลางระหว่างศัตรู 2 ตัว ---
    const r1 = row - dr, c1 = col - dc
    const r2 = row + dr, c2 = col + dc
    
    if (
      inBounds(r1, c1) && inBounds(r2, c2) &&
      board.value[r1][c1] === enemy &&
      board.value[r2][c2] === enemy
    ) {
      board.value[r1][c1] = ''
      board.value[r2][c2] = ''
      captured += 2
    }
    
    // --- รูปแบบที่ 2: หนีบศัตรูหลายตัวระหว่างหมากเรา 2 ตัว ---
    let toCapture = []
    let r = row + dr
    let c = col + dc
    
    while (inBounds(r, c) && board.value[r][c] === enemy) {
      toCapture.push([r, c])
      r += dr
      c += dc
    }
    
    // ถ้ามีศัตรูคั่นกลางอย่างน้อย 1 ตัว และปลายทางเป็นหมากเรา
    if (
      toCapture.length > 0 &&
      inBounds(r, c) &&
      board.value[r][c] === currentPlayer.value
    ) {
      for (const [cr, cc] of toCapture) {
        board.value[cr][cc] = ''
        captured++
      }
    }
  }
  
  // เพิ่มคะแนนให้ฝั่งที่เดิน
  if (captured > 0) {
    if (currentPlayer.value === 'X') {
      xScore.value += captured
    } else {
      oScore.value += captured
    }
    checkGameEnd()
  }
}

function switchPlayer() {
  currentPlayer.value = currentPlayer.value === 'X' ? 'O' : 'X'
  turnStartTime.value = timeLeft.value // บันทึกเวลาตอนเริ่มเทิร์นใหม่
  
  // ถ้าไม่ใช่ PvP ให้ AI เดิน
  if (!isPvP.value && currentPlayer.value === 'O') {
    requestAIMove()
  }
}

async function requestAIMove() {
  try {
    const response = await axios.post('http://localhost:5000/ai/move', {
      boardState: getBoardState(),
      difficulty: difficulty.value, // หรือ props.difficulty ถ้าใช้ defineProps
      timeLeft: timeLeft.value
    })
    
    const { from, to, thoughts } = response.data
    
    if (from && to) {
      const [fr, fc] = from
      const [tr, tc] = to
      
      board.value[tr][tc] = board.value[fr][fc]
      board.value[fr][fc] = ''
      checkCapture(tr, tc)
      
      // เพิ่มความคิดใหม่เข้าไปในประวัติ
      aiThoughtHistory.value.unshift({
        turn: aiThoughtHistory.value.length + 1,
        thoughts,
        timestamp: new Date().toLocaleTimeString()
      })
    }
  } catch (err) {
    console.error('AI move error:', err)
  } finally {
    currentPlayer.value = 'X'
  }
}

// เรียกใช้เมื่อจบเกม
async function saveGameHistory() {
  // สมมติคุณเก็บประวัติการเดินไว้ใน moveHistory (array)
  // และมีตัวแปร winner, xScore, oScore, xMoveCount, oMoveCount, xTotalTime, oTotalTime, difficultyText
  try {
    await axios.post('http://localhost:5000/save-history', {
      moves: moveHistory.value,
      winner: winner.value,
      xMoveCount: moveHistory.value.filter(m => m.player === 'X').length,
      oMoveCount: moveHistory.value.filter(m => m.player === 'O').length,
      xScore: xScore.value, // <-- แต้มที่ X ทำได้
      oScore: oScore.value, // <-- แต้มที่ O ทำได้
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

setInterval(() => {
  if (timeLeft.value > 0) {
    timeLeft.value--
    if (timeLeft.value === 0) checkGameEnd()
  }
}, 1000)

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
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap');

.game-container {
  font-family: 'Kanit', sans-serif;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, #2d0a0a 0%, #0a0000 70%);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 1rem;
  box-sizing: border-box;
}

.fire-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 25% 75%, rgba(255, 69, 0, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 75% 25%, rgba(255, 140, 0, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(220, 20, 60, 0.08) 0%, transparent 70%),
    linear-gradient(45deg, 
      transparent 0%,
      rgba(139, 0, 0, 0.2) 25%,
      rgba(255, 69, 0, 0.15) 50%,
      rgba(139, 0, 0, 0.2) 75%,
      transparent 100%);
  background-size: 400% 400%, 300% 300%, 500% 500%, 200% 200%;
  animation: 
    fireEffect1 12s ease-in-out infinite,
    fireEffect2 18s ease-in-out infinite reverse,
    fireEffect3 25s ease-in-out infinite;
  opacity: 0.6;
}

.ambient-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(1px 1px at 20px 30px, rgba(255, 69, 0, 0.4), transparent),
    radial-gradient(1px 1px at 40px 70px, rgba(255, 140, 0, 0.3), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(255, 215, 0, 0.2), transparent),
    radial-gradient(1px 1px at 130px 80px, rgba(255, 69, 0, 0.2), transparent);
  background-repeat: repeat;
  background-size: 250px 150px;
  animation: sparkle 30s linear infinite;
  opacity: 0.4;
}

.content {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 2rem;
  max-width: 1600px;
}

.ai-thoughts-panel {
  height: 100%;
  background: linear-gradient(145deg, rgba(30, 30, 30, 0.95), rgba(20, 20, 20, 0.9));
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.ai-icon {
  font-size: 2rem;
  animation: pulse 2s ease-in-out infinite;
}

.panel-title {
  color: #e0e0e0;
  font-size: 1.5rem;
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
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.thought-entry.latest {
  border-color: rgba(255, 215, 0, 0.3);
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.1);
}

.thought-entry::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, rgba(255, 215, 0, 0.5), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.thought-entry.latest::before {
  opacity: 1;
}

.thought-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  color: #b0b0b0;
  font-size: 0.9rem;
}

.turn-number {
  font-weight: 600;
  color: #ffd700;
}

.timestamp {
  opacity: 0.7;
  font-size: 0.8rem;
}

.thought-content {
  color: #e0e0e0;
  line-height: 1.6;
  white-space: pre-wrap;
  font-size: 0.95rem;
}

.empty-thoughts {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  color: #888;
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
  background: #666;
  border-radius: 50%;
  animation: thinking 1.4s ease-in-out infinite both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

.game-content {
  background: linear-gradient(145deg, rgba(20, 5, 5, 0.95), rgba(10, 0, 0, 0.9));
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 2rem;
  box-shadow: 
    0 20px 40px rgba(255, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 69, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden;
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
  text-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
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
  gap: 2rem;
}

.info-card {
  flex: 1 1 0;
  min-width: 0;
  max-width: none;
  background: linear-gradient(135deg, rgba(255,255,255,0.10), rgba(255,255,255,0.05));
  border-radius: 16px;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.7rem;
  border: 1px solid rgba(255,255,255,0.1);
  box-sizing: border-box;
}

.info-card .info-content {
  width: 100%;
  text-align: center;
}

.info-icon {
  font-size: 2rem;
  opacity: 0.8;
}

.info-content {
  flex: 1;
}

.info-label {
  color: #b0b0b0;
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
  color: #ffa726;
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
  font-size: 1.2rem;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
}

.game-board-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
}

.board {
  position: relative;
  display: grid;
  grid-template-rows: repeat(8, 1fr);
  gap: 3px;
  background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
  padding: 20px;
  border-radius: 20px;
  border: 3px solid rgba(255, 69, 0, 0.3);
  box-shadow: 
    0 0 40px rgba(255, 69, 0, 0.2),
    inset 0 0 20px rgba(0, 0, 0, 0.5);
  user-select: none;
}

.board-border {
  position: absolute;
  top: -3px;
  left: -3px;
  right: -3px;
  bottom: -3px;
  border-radius: 20px;
  background: linear-gradient(45deg, 
    rgba(255, 69, 0, 0.3), 
    rgba(255, 140, 0, 0.2), 
    rgba(255, 69, 0, 0.3));
  background-size: 200% 200%;
  animation: borderGlow 3s ease-in-out infinite;
  z-index: -1;
}

.row {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 3px;
}

.cell {
  width: 61px;
  height: 61px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 11px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  outline-offset: 4px;
  overflow: hidden;
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
  font-size: 0.7rem;
  color: rgba(255, 255, 255, 0.3);
  font-weight: 500;
  pointer-events: none;
}

.cell:hover:not(.selected):not(.has-piece) {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
}

.cell:focus-visible {
  outline: 3px solid #ffd700;
  outline-offset: 3px;
  z-index: 10;
}

.cell-black {
  background: linear-gradient(145deg, #2d2d2d, #1a1a1a);
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
}

.cell-red {
  background: linear-gradient(145deg, #4a1a1a, #2d0d0d);
  box-shadow: inset 0 2px 4px rgba(139, 0, 0, 0.2);
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
  top: 15%;
  left: 15%;
  right: 15%;
  bottom: 15%;
  border-radius: 50%;
  background: inherit;
  filter: brightness(1.2);
}

.piece-shine {
  position: absolute;
  top: 20%;
  left: 25%;
  width: 30%;
  height: 30%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.4), transparent);
  border-radius: 50%;
  filter: blur(2px);
}

.piece-black {
  background: linear-gradient(145deg, #4a4a4a, #1a1a1a);
  border: 2px solid #666;
  box-shadow: 
    0 4px 8px rgba(0, 0, 0, 0.5),
    inset 0 2px 4px rgba(255, 255, 255, 0.1);
}

.piece-red {
  background: linear-gradient(145deg, #ff4444, #cc0000);
  border: 2px solid #ff6666;
  box-shadow: 
    0 4px 8px rgba(204, 0, 0, 0.5),
    inset 0 2px 4px rgba(255, 255, 255, 0.2);
}

.selected {
  box-shadow: 
    inset 0 0 20px rgba(255, 215, 0, 0.6),
    0 0 30px rgba(255, 215, 0, 0.4);
  transform: scale(1.1);
  z-index: 5;
}

.selected .piece {
  transform: scale(1.1);
  box-shadow: 
    0 0 25px rgba(255, 215, 0, 0.6),
    0 4px 8px rgba(0, 0, 0, 0.3);
}

.possible-move {
  box-shadow: inset 0 0 15px rgba(76, 175, 80, 0.6);
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

.score-board {
  display: flex;
  align-items: center;
  gap: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.score-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border-radius: 16px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  transition: all 0.3s ease;
}

.score-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.score-icon {
  font-size: 1.5rem;
}

.score-content {
  text-align: center;
}

.score-label {
  color: #b0b0b0;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.score-value {
  color: #fff;
  font-size: 1.8rem;
  font-weight: 700;
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
  background: linear-gradient(135deg, #ff4444, #cc0000);
  border: none;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  padding: 1rem 2rem;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 0 4px 15px rgba(255, 68, 68, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  user-select: none;
  font-family: 'Kanit', sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.control-button:hover {
  background: linear-gradient(135deg, #ff6666, #ff4444);
  box-shadow: 0 8px 25px rgba(255, 68, 68, 0.4);
  transform: translateY(-3px);
}

.control-button:active {
  transform: translateY(-1px);
}

.control-button .icon {
  font-size: 1.2rem;
}

.game-over-overlay {
  position: relative;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

.game-over-panel {
  background: linear-gradient(145deg, rgba(30, 30, 30, 0.95), rgba(20, 20, 20, 0.9));
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.5),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  text-align: center;
  min-width: 400px;
  animation: slideUp 0.4s ease;
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
  color: #ffa726;
}

.result-text.winner {
  color: #4caf50;
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
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
}

.final-score {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.final-score-label {
  color: #b0b0b0;
  font-size: 0.9rem;
}

.final-score-value {
  color: #fff;
  font-size: 1.5rem;
  font-weight: 700;
}

.game-over-button {
  width: 100%;
  justify-content: center;
}

/* Custom Scrollbar */
.thoughts-history::-webkit-scrollbar {
  width: 6px;
}

.thoughts-history::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 3px;
}

.thoughts-history::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
}

.thoughts-history::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* Animations */
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
  0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.4; }
  50% { transform: translateY(-15px) rotate(180deg); opacity: 0.8; }
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.05); }
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

@keyframes thinking {
  0%, 80%, 100% { transform: scale(0); opacity: 0.5; }
  40% { transform: scale(1); opacity: 1; }
}

@keyframes borderGlow {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

@keyframes possibleMove {
  0%, 100% { box-shadow: inset 0 0 15px rgba(76, 175, 80, 0.6); }
  50% { box-shadow: inset 0 0 25px rgba(76, 175, 80, 0.8); }
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

/* Responsive Design */
@media (max-width: 1200px) {
  .content {
    grid-template-columns: 1fr;
    grid-template-rows: 300px 1fr;
  }
  
  .ai-thoughts-panel {
    height: 300px;
  }
}

@media (max-width: 768px) {
  .content {
    padding: 1rem;
    gap: 1rem;
  }
  
  .cell {
    width: 45px;
    height: 45px;
  }
  
  .board {
    padding: 15px;
  }
  
  .game-info {
    grid-template-columns: 1fr;
    gap: 1rem;
  }
  
  .difficulty-display {
    font-size: 1.5rem;
  }
  
  .score-board {
    flex-direction: column;
    gap: 1rem;
  }
  
  .game-status-bar {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
  .info-card {
    min-width: 0;
    width: 100%;
    max-width: 400px;
  }
  
  .game-over-panel {
    margin: 1rem;
    padding: 2rem;
    min-width: auto;
  }
}

@media (max-width: 480px) {
  .cell {
    width: 35px;
    height: 35px;
  }
  
  .game-content {
    padding: 1.5rem;
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
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .fire-background,
  .ambient-particles,
  .difficulty-icon,
  .ai-icon,
  .thinking-animation,
  .border-glow,
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

/* Focus states for accessibility */
.control-button:focus {
  outline: 3px solid rgba(255, 215, 0, 0.6);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .cell-black {
    background: #000;
    border: 2px solid #fff;
  }
  
  .cell-red {
    background: #800000;
    border: 2px solid #fff;
  }
  
  .piece-black {
    background: #000;
    border: 3px solid #fff;
  }
  
  .piece-red {
    background: #ff0000;
    border: 3px solid #fff;
  }
}
</style>
