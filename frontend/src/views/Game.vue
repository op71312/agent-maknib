<template>
  <div class="game-container">
    <!-- Background elements are now fixed to the viewport -->
    <div class="fire-background"></div>
    <div class="ambient-particles"></div>
    
    <!-- REMOVED: Back Button (top one) as requested. The back button at the bottom of the board will be used instead. -->
    
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
                    {{ currentPlayer === 'X' ? 'ผู้เล่น ⚫' : (isPvP ? 'ผู้เล่น 🔴' : 'AI (O) 🔴') }}
                  </div>
                </div>
              </div>
              
              <!-- คะแนน -->
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
                  <!-- ลบหรือคอมเมนต์บรรทัดนี้ในแต่ละ .cell -->
                  <!-- <div class="cell-coordinates">{{ String.fromCharCode('a'.charCodeAt(0) + colIndex) }}{{ 8 - rowIndex }}</div> -->
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

          <!-- ปุ่มกลับขวาล่าง -->
          <button class="control-button back-float-btn" @click="goBack" aria-label="กลับสู่เมนูระดับ">
            <i class="icon">🏠</i>
            <span>กลับ</span>
          </button>
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
import { ref, computed, onUnmounted } from 'vue'
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
  ];

  const enemy = currentPlayer.value === 'X' ? 'O' : 'X';
  let captured = 0;

  for (const [dr, dc] of dirs) {
    // --- หนีบศัตรูหลายตัวระหว่างหมากเรา 2 ตัว (เช่น _ x x x o) ---
    let toCapture = [];
    let r = row + dr;
    let c = col + dc;
    while (inBounds(r, c) && board.value[r][c] === enemy) {
      toCapture.push([r, c]);
      r += dr;
      c += dc;
    }
    // ถ้ามีศัตรูคั่นกลางอย่างน้อย 1 ตัว และปลายทางเป็นหมากเรา
    if (
      toCapture.length > 0 &&
      inBounds(r, c) &&
      board.value[r][c] === currentPlayer.value
    ) {
      for (const [cr, cc] of toCapture) {
        board.value[cr][cc] = '';
        captured++;
      }
    }

    // --- กติกา "แทรก" ไม่จำกัดจำนวนช่อง ---
    // เช่น x o o o _ o x แล้ว o มาแทรก
    // ตรวจสอบฝั่งซ้าย/บนและขวา/ล่างเป็นศัตรู ตรงกลางเป็นหมากเรา
    let leftR = row - dr, leftC = col - dc;
    let rightR = row + dr, rightC = col + dc;
    let midCount = 0;
    // เดินไปทางขวา/ล่าง นับหมากเรา
    while (inBounds(rightR, rightC) && board.value[rightR][rightC] === currentPlayer.value) {
      midCount++;
      rightR += dr;
      rightC += dc;
    }
    // เดินไปทางซ้าย/บน นับหมากเรา
    let leftCount = 0;
    while (inBounds(leftR, leftC) && board.value[leftR][leftC] === currentPlayer.value) {
      leftCount++;
      leftR -= dr;
      leftC -= dc;
    }
    // ถ้าทั้งสองฝั่งเป็นศัตรู และตรงกลางเป็นหมากเราอย่างน้อย 1 ตัว
    if (
      midCount + leftCount > 0 &&
      inBounds(leftR, leftC) && inBounds(rightR, rightC) &&
      board.value[leftR][leftC] === enemy &&
      board.value[rightR][rightC] === enemy
    ) {
      board.value[leftR][leftC] = '';
      board.value[rightR][rightC] = '';
      captured += 2;
    }

    // --- เพิ่มกรณี sandwich สั้น (enemy - me - enemy) ---
    // ใช้ชื่อใหม่เพื่อไม่ชนกับตัวแปรข้างบน
    const sLeftR = row - dr, sLeftC = col - dc;
    const sRightR = row + dr, sRightC = col + dc;
    if (
      inBounds(sLeftR, sLeftC) && inBounds(sRightR, sRightC) &&
      board.value[sLeftR][sLeftC] === enemy &&
      board.value[sRightR][sRightC] === enemy
    ) {
      board.value[sLeftR][sLeftC] = '';
      board.value[sRightR][sRightC] = '';
      captured += 2;
    }
  }

  // เพิ่มคะแนนให้ฝั่งที่เดิน
  if (captured > 0) {
    if (currentPlayer.value === 'X') {
      xScore.value += captured;
    } else {
      oScore.value += captured;
    }
    checkGameEnd();
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
    const response = await axios.post('http://localhost:8000/ai-move', {
      board: getBoardState(),
      current_player: 1 // ฝั่ง AI คือ 1 (O) ตาม convention ของโมเดล
    })
    const { from_row, from_col, to_row, to_col, action_id } = response.data
    // เดินหมากตามที่ AI ตอบกลับ
    board.value[to_row][to_col] = board.value[from_row][from_col]
    board.value[from_row][from_col] = ''
    checkCapture(to_row, to_col)
    // เพิ่มประวัติความคิด AI (ถ้ามี)
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

// Ensure all hooks are called at the top level
startTimer()

onUnmounted(() => {
  clearInterval(timerInterval.value)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap');

.game-container {
  font-family: 'Kanit', sans-serif;
  /* Ensure it takes full viewport width and height */
  position: fixed; /* ADDED: Fix position to viewport */
  top: 0; /* ADDED: Align to top */
  left: 0; /* ADDED: Align to left */
  width: 100vw; /* ADDED: Take full viewport width */
  height: 100vh; /* Changed from min-height to height for full coverage */
  background: radial-gradient(ellipse at center, #1a0000 0%, #000000 70%);
  overflow-y: auto; /* Allow scrolling on the main container */
  display: flex; /* Use flexbox for main layout */
  flex-direction: column; /* Stack children vertically */
  justify-content: flex-start; /* Align content to the top */
  align-items: center; /* Center content horizontally */
  /* REMOVED: padding: 1rem; from here */
  box-sizing: border-box;
}

.fire-background,
.ambient-particles {
  position: fixed; /* Keep fixed for background */
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  transform: translateZ(0); /* Promote hardware acceleration */
}

/* REMOVED: .back-btn and .back-btn-icon CSS rules as the top button is removed from template */

.content {
  position: relative;
  z-index: 1;
  width: 100%; /* Ensure it takes full width of its parent */
  flex-grow: 1; /* Allow content to grow and fill vertical space */
  display: grid; /* Desktop layout */
  grid-template-columns: 350px 1fr;
  gap: 2rem;
  padding: 2rem; /* ADDED: Padding moved here for internal spacing */
  /* REMOVED: max-width: 1800px; to allow full width stretch */
  transform: translateZ(0);
  /* Ensure content area is at least viewport height minus padding */
  min-height: calc(100vh - 4rem); /* Adjusted for 2rem padding on top/bottom */
}

.ai-thoughts-panel {
  height: 100%; /* Make it stretch to the height of the content grid area */
  background: linear-gradient(145deg,  rgba(97, 26, 26, 0.95), rgba(10, 0, 0, 0.98)); /* Increased opacity */
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 
    0 10px 20px rgba(255, 0, 0, 0.15), /* Reduced shadow blur */
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 69, 0, 0.2);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Keep hidden for the panel itself, thoughts-history handles scroll */
  transform: translateZ(0); /* Promote hardware acceleration */
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
  overflow-y: auto; /* This is the scrollbar for the AI thoughts content */
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
  height: 100%; /* Make it stretch to the height of the content grid area */
  background: linear-gradient(145deg, rgba(97, 26, 26, 0.95), rgba(10, 0, 0, 0.98)); /* Increased opacity */
  border-radius: 20px;
  padding: 2rem;
  box-shadow: 
    0 10px 20px rgba(186, 41, 41, 0.1),
    inset 0 1px 0 rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 69, 0, 0.13);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Keep hidden for the panel itself, board-container handles scroll */
  transform: translateZ(0); /* Promote hardware acceleration */
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
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
  min-height: 0; /* Allow flex item to shrink */
  overflow-y: auto; /* Allow internal scrolling for the board and controls if needed */
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
  filter: blur(4px); /* Reduced blur for performance */
  transform: translateZ(0); /* Promote hardware acceleration */
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
  transform: translateZ(0); /* Promote hardware acceleration */
}

.game-over-panel {
  background: linear-gradient(145deg, rgba(30, 0, 0, 0.95), rgba(10, 0, 0, 0.98)); /* Increased opacity */
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 
    0 10px 20px rgba(255, 0, 0, 0.25), /* Reduced shadow blur */
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 69, 0, 0.3);
  text-align: center;
  min-width: 400px;
  animation: slideUp 0.4s ease;
  transform: translateZ(0); /* Promote hardware acceleration */
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

.game-over-button {
  width: 100%;
  justify-content: center;
}

/* Custom Scrollbar */
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

/* Responsive Design */
@media (max-width: 1400px) {
  .content {
    grid-template-columns: 320px 1fr;
  }
}

@media (max-width: 1200px) {
  .content {
    grid-template-columns: 1fr; /* Single column */
    display: flex; /* Use flexbox for vertical stacking */
    flex-direction: column;
    gap: 1.5rem; /* Adjust gap for mobile */
    padding-top: 2rem; /* Adjusted padding as fixed back-btn is removed, keeping 2rem top padding */
    height: auto; /* Allow content to define its height */
    min-height: auto; /* Reset min-height for mobile flex layout */
    overflow-y: auto; /* Allow content area to scroll on mobile */
  }
  
  .ai-thoughts-panel,
  .game-content {
    flex-shrink: 0; /* Prevent shrinking below content size */
    flex-grow: 1; /* Allow them to grow */
    min-height: 0; /* Crucial for flex items to shrink */
    height: auto; /* Let content define height */
  }

  /* Make game-content scrollable on mobile */
  .game-content {
    overflow-y: auto; 
  }
}

@media (max-width: 768px) {
  .content {
    padding: 1rem; /* Adjusted padding for smaller screens */
    gap: 1rem;
    padding-top: 1rem; /* Adjusted padding for smaller screens */
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

/* Accessibility improvements */
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

/* Focus states for accessibility */
.control-button:focus {
  outline: 3px solid rgba(255, 215, 0, 0.6);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .cell-light {
    background: #f5deb3;
    border: 2px solid #000;
  }
  
  .cell-dark {
    background: #8b4513;
    border: 2px solid #000;
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

.back-float-btn {
  position: absolute;
  right: 2rem;
  bottom: 2rem;
  z-index: 20;
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

@media (max-width: 768px) {
  .back-float-btn {
    right: 1rem;
    bottom: 1rem;
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
  }
}
</style>
