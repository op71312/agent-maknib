<template>
  <div class="game-container">
    <div class="fire-background"></div>
    <div class="content">
      <!-- AI Thoughts Panel -->
      <div class="ai-thoughts-panel">
        <h3 class="panel-title">AI's Analysis</h3>
        <div class="thoughts-history">
          <div v-for="(entry, index) in aiThoughtHistory" 
               :key="index"
               class="thought-entry">
            <div class="thought-header">
              <span class="turn-number">Turn {{entry.turn}}</span>
              <span class="timestamp">{{entry.timestamp}}</span>
            </div>
            <div class="thought-content">
              {{entry.thoughts}}
            </div>
          </div>
        </div>
      </div>

      <!-- Game Content -->
      <div class="game-content">
        <h2 class="difficulty-display">ระดับ: {{ difficultyText }}</h2>

        <div class="game">
          <div class="game-info">
            <div class="timer" :aria-label="'เวลาที่เหลือ: ' + Math.floor(timeLeft / 60) + ' นาที ' + (timeLeft % 60) + ' วินาที'">
              ⏳ เวลา: {{ Math.floor(timeLeft / 60) }}:{{ (timeLeft % 60).toString().padStart(2, '0') }}
            </div>
            <div class="turn">ถึงตา: 
              <span class="player-name">
                {{ currentPlayer === 'X' ? 'ผู้เล่น X' : (isPvP ? 'ผู้เล่น O' : 'AI (O)') }}
              </span>
            </div>
          </div>

          <div class="board" role="grid" aria-label="กระดานเกม">
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
                  'possible-move': isPossibleMove(rowIndex, colIndex)
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
                </div>
              </div>
            </div>
          </div>

          <div class="score-board">
            <span class="score-x">X: {{ xScore }}</span>
            <span class="score-o">O: {{ oScore }}</span>
          </div>

          <button class="back-button" @click="goBack" aria-label="กลับสู่เมนูระดับ">
            กลับ
          </button>
        </div>

        <!-- Game Over Panel -->
        <div v-if="isGameOver" class="game-over-panel">
          <h2>จบเกม</h2>
          <p v-if="winner === 'draw'">เสมอ</p>
          <p v-else>ผู้ชนะ: {{ winner }}</p>
          <button class="back-button" @click="goBack">กลับ</button>
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
      xScore: xScore.value,      // <-- แต้มที่ X ทำได้
      oScore: oScore.value,      // <-- แต้มที่ O ทำได้
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
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;700&display=swap');

.game-container {
  font-family: 'Kanit', sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #1a0a0a;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
}

.fire-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(45deg, 
    transparent 0%,
    #440000 45%,
    #bb0000 55%,
    transparent 100%);
  background-size: 200% 200%;
  animation: fireEffect 12s ease infinite;
  opacity: 0.45;
  filter: blur(15px);
  z-index: 0;
}

.content {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: 400px 1fr;
  gap: 2rem;
  padding: 2rem;
}

.ai-thoughts-panel {
  height: 93vh;
  background: rgba(172, 63, 63, 0.7);
  backdrop-filter: blur(12px);
  border-radius: 30px;
  padding: 3rem;
  box-shadow: 0 8px 32px rgba(175, 68, 68, 0.3);
  border: 5px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
}

.panel-title {
  color: #fecaca;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  text-align: center;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

.thoughts-history {
  flex: 1;
  overflow-y: auto;
  padding-right: 1rem;
}

.thought-entry {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.thought-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.8rem;
  color: #fecaca;
  font-size: 0.9rem;
}

.turn-number {
  font-weight: 600;
}

.timestamp {
  opacity: 0.8;
}

.thought-content {
  color: #fff;
  line-height: 1.6;
  white-space: pre-wrap;
  font-size: 1rem;
}

/* Custom Scrollbar */
.thoughts-history::-webkit-scrollbar {
  width: 8px;
}

.thoughts-history::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 4px;
}

.thoughts-history::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 4px;
}

.thoughts-history::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.3);
}

.game-content {
  background: rgba(30, 0, 0, 0.85);
  padding: 2.5rem 3rem;
  border-radius: 20px;
  box-shadow: 0 0 40px rgba(255, 0, 0, 0.7);
  border: 2px solid #cc0000;
  user-select: none;
}

.difficulty-display {
  color: #ff4747;
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1.5rem;
  text-shadow: 0 0 15px #ff0000;
  letter-spacing: 1px;
  text-align: center;
}

.game-info {
  display: flex;
  justify-content: space-between;
  color: #ffaaaa;
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
  text-shadow: 0 0 6px #aa0000;
}

.timer {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.turn {
  font-style: italic;
  color: #ffeaea;
}

.player-name {
  font-weight: 700;
  color: #ffdddd;
  text-shadow: 0 0 10px #ff5555;
}

.game {
  max-width: 720px;
  margin: 0 auto;
  text-align: center;
}

.board {
  display: grid;
  grid-template-rows: repeat(8, 1fr);
  gap: 2px;
  background: #330000;
  padding: 12px;
  border-radius: 14px;
  border: 4px solid #660000;
  box-shadow: 0 0 30px rgba(204, 0, 0, 0.6);
  margin-bottom: 1.8rem;
  user-select: none;
}

.row {
  display: grid;
  grid-template-columns: repeat(8, 1fr);
  gap: 2px;
}

.cell {
  width: 72px;
  height: 72px;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  border-radius: 8px;
  transition: transform 0.15s ease, box-shadow 0.3s ease;
  box-shadow: inset 0 0 0 1px #440000;
  position: relative;
  outline-offset: 4px;
}

.cell:hover:not(.selected) {
  transform: scale(1.05);
  box-shadow: 0 0 12px #ff5555;
  z-index: 2;
}

.cell:focus-visible {
  outline: 3px solid #ff4444;
  outline-offset: 3px;
  z-index: 3;
}

.cell-black {
  background-color: #1a1a1a;
}

.cell-red {
  background-color: #550000;
}

.piece {
  width: 84%;
  height: 84%;
  border-radius: 50%;
  box-shadow: 0 0 15px rgba(0, 0, 0, 0.7);
  transition: transform 0.3s ease, box-shadow 0.4s ease;
}

.piece-black {
  background: linear-gradient(145deg, #222222, #000000);
  border: 2.5px solid #660000;
  box-shadow: 0 0 20px #aa0000;
}

.piece-red {
  background: linear-gradient(145deg, #ff2222, #bb0000);
  border: 2.5px solid #ff4444;
  box-shadow: 0 0 20px #ff3333;
}

.selected {
  box-shadow: inset 0 0 20px #ffd700, 0 0 20px #ffd700;
  transform: scale(1.1);
  z-index: 5;
}

.selected .piece {
  transform: scale(1.05);
  box-shadow: 0 0 30px #ffd700;
}

.possible-move {
  box-shadow: inset 0 0 18px rgba(255, 215, 0, 0.85);
  border-radius: 8px;
  transition: box-shadow 0.3s ease;
}

.back-button {
  background: linear-gradient(90deg, #cc0000, #ff4444);
  border: none;
  color: white;
  font-weight: 700;
  font-size: 1.3rem;
  padding: 12px 28px;
  border-radius: 40px;
  cursor: pointer;
  box-shadow: 0 0 25px #ff4444;
  transition: background 0.4s ease, box-shadow 0.3s ease;
  user-select: none;
  display: inline-block;
  margin: 0 auto;
}

.back-button:hover {
  background: linear-gradient(90deg, #ff4444, #cc0000);
  box-shadow: 0 0 35px #ff6666;
  transform: scale(1.05);
}

@keyframes fireEffect {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

@media (max-width: 768px) {
  .cell {
    width: 50px;
    height: 50px;
  }

  .board {
    padding: 8px;
    border-width: 3px;
  }

  .game-info {
    font-size: 1.3rem;
  }

  .difficulty-display {
    font-size: 2rem;
  }

  .back-button {
    font-size: 1.1rem;
    padding: 10px 22px;
  }
}

@media (max-width: 480px) {
  .cell {
    width: 38px;
    height: 38px;
  }

  .game-content {
    padding: 1.5rem 2rem;
  }

  .difficulty-display {
    font-size: 1.6rem;
  }
}

@media (max-width: 1200px) {
  .content {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
  }

  .ai-thoughts-panel {
    height: 300px;
  }
}

.score-board {
  display: flex;
  justify-content: center;
  gap: 2rem;
  font-size: 1.3rem;
  margin-bottom: 1rem;
}
.score-x { color: #fff176; font-weight: bold; }
.score-o { color: #ef5350; font-weight: bold; }

.game-over-panel {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(50, 50, 50, 0.9);
  border-radius: 20px;
  padding: 2rem 3rem;
  box-shadow: 0 0 40px rgba(0, 0, 0, 0.8);
  z-index: 1000;
  text-align: center;
}

.game-over-panel h2 {
  color: #ff4747;
  font-size: 2.5rem;
  margin-bottom: 1rem;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.1);
}

.game-over-panel p {
  color: #fff;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
}

.game-over-panel .back-button {
  width: 100%;
  padding: 12px 0;
  font-size: 1.2rem;
}
</style>
