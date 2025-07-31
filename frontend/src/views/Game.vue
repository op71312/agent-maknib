<template>
  <div class="game-container">
    <!-- Background elements are now fixed to the viewport -->
    <div class="fire-background"></div>
    <div class="ambient-particles"></div>
    
    <div class="content" :class="{ 'pvp-mode': isPvP, 'prompt-mode': isPromptMode, 'triple-panel': showStrategyPanel && showAIAnalysisPanel }">
      <!-- AI Thoughts Panel (แสดงในทุกโหมดที่ไม่ใช่ PvP) -->
      <div v-if="showAIAnalysisPanel" class="ai-thoughts-panel">
        <div class="panel-header">
          <div class="ai-icon">🤖</div>
          <h3 class="panel-title">AI's Analysis</h3>
        </div>
        <div class="thoughts-history">
          <!-- แสดงสถานะ Auto-play ในโหมด Prompt -->
          <div v-if="isPromptMode && isAutoPlayActive" class="auto-play-status">
            <div class="status-header">
              <span class="status-icon">🤖</span>
              <h4>Auto-play กำลังดำเนินการ</h4>
            </div>
            <div class="status-details">
              <p>ตาที่: {{ autoPlayTurnCount + 1 }} / {{ maxAutoPlayTurns }}</p>
              <p>กลยุทธ์ X: {{ selectedStrategy }}</p>
              <p>กลยุทธ์ O: {{ llmStrategy || 'กำลังวิเคราะห์...' }}</p>
              <button class="stop-auto-play-btn" @click="stopAutoPlay">หยุด Auto-play</button>
            </div>
          </div>
          
          <div v-for="(entry, index) in aiThoughtHistory"
               :key="index"
               class="thought-entry"
               :class="{ 'latest': index === 0, 'processing': entry.isProcessing }">
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

      <!-- Game Content (main area) -->
      <div class="game-content">
        <div class="game-header">
          <!-- เพิ่ม container สำหรับ header ให้มีปุ่มกลับอยู่ชิดขวา -->
          <div class="header-container">
            <div class="difficulty-header">
              <h2 class="difficulty-display">
                <span class="difficulty-icon">⚔️</span>
                ระดับ: {{ difficultyText }}
              </h2>
            </div>
            
            <!-- ย้ายปุ่มกลับมาไว้ชิดขวา -->
            <button class="control-button back-btn corner" @click="goBack" aria-label="กลับสู่เมนูระดับ">
              <i class="icon">🏠</i>
              <span>กลับ</span>
            </button>
          </div>
          
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
                    {{ currentPlayer === 'X' ? 'ผู้เล่น ⚫' : (isPvP ? 'ผู้เล่น 🔴' : 'AI 🔴') }}
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
          <!-- ลบปุ่มกลับที่เคยอยู่ตรงนี้ -->
          <div class="board-wrapper">
            <!-- กระดานเกม -->
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
        </div>

        <!-- Game Over Panel -->
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
              <!-- โหมดเล่นกับ AI -->
              <p v-if="!isPvP && winner === 'O'" class="result-text loser">
                คุณแพ้ AI 😢
              </p>
              <p v-else-if="!isPvP && winner === 'X'" class="result-text winner">
                คุณชนะ AI! 🎉
              </p>
              <!-- โหมดเล่นกับเพื่อน -->
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
            <!-- เพิ่มปุ่มกลับ -->
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

      <!-- Prompt Panel (แสดงในทุกโหมดที่ไม่ใช่ PvP) -->
      <div v-if="showStrategyPanel" class="prompt-panel">
        <div class="panel-header">
          <div class="prompt-icon">💡</div>
          <h3 class="panel-title">กลยุทธ์พิเศษ</h3>
        </div>
        <div class="prompt-content">
          <div class="strategies-filter">
            <select v-model="selectedCategory" class="strategy-select">
              <option value="all">ทั้งหมด</option>
              <option value="ชนะศึก">กลยุทธ์ชนะศึก</option>
              <option value="เผชิญศึก">กลยุทธ์เผชิญศึก</option>
              <option value="เข้าตี">กลยุทธ์เข้าตี</option>
              <option value="ติดพัน">กลยุทธ์ติดพัน</option>
              <option value="ร่วมรบ">กลยุทธ์ร่วมรบ</option>
              <option value="ยามพ่าย">กลยุทธ์ยามพ่าย</option>
            </select>
            <div class="strategy-search">
              <input type="text" v-model="strategySearch" placeholder="ค้นหากลยุทธ์..." class="strategy-search-input">
            </div>
          </div>
          <div class="strategy-list">
            <div v-for="(strategy, index) in filteredStrategies" :key="index" class="strategy-item">
              <div class="strategy-header">
                <button v-if="showApplyButton" 
                        class="strategy-btn top-left" 
                        @click="applyStrategy(index)"
                        :disabled="isAutoPlayActive">
                  {{ isAutoPlayActive ? 'กำลังเล่น...' : 'นำไปใช้' }}
                </button>
                <div class="strategy-title-container">
                  <span class="strategy-title"><strong>{{strategy.name}}</strong></span>
                </div>
              </div>
              <p class="strategy-description">
                {{ strategy.description }}
              </p>
              <div class="strategy-category">{{ strategy.category }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted, onMounted } from 'vue'
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
    validator: (val) => ['easy', 'medium', 'hard', 'prompt', 'friend'].includes(val) // Added 'prompt'
  }
})

const difficultyText = computed(() => {
  const map = {
    easy: 'ง่าย',
    medium: 'กลาง',
    hard: 'ยาก',
    prompt: 'พรอมต์', // Added 'prompt'
    friend: 'เล่นกับเพื่อน'
  }
  return map[difficulty.difficulty]
})

const isPvP = computed(() => difficulty.difficulty === 'friend')
const isPromptMode = computed(() => difficulty.difficulty === 'prompt')

const userPrompt = ref('') // New ref for prompt input

// Prompt mode variables
const isAutoPlayActive = ref(false)
const autoPlayTurnCount = ref(0)
const maxAutoPlayTurns = ref(10) // 5 rounds each side = 10 turns total
const selectedStrategy = ref('')
const selectedStrategyActions = ref([])
const actionIndex = ref(0)
const llmStrategy = ref('')
const llmActions = ref([])
const llmActionIndex = ref(0)

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

const timerInterval = ref(null)

const startTimer = () => {
  timerInterval.value = setInterval(() => {
    if (timeLeft.value > 0) {
      timeLeft.value--
      if (timeLeft.value === 0) checkGameEnd()
    }
  }, 1000)
}

const initializeGame = () => {
  startTimer()
}

initializeGame()

onUnmounted(() => {
  clearInterval(timerInterval.value)
  // หยุด auto-play ถ้ากำลังทำงานอยู่
  if (isAutoPlayActive.value) {
    stopAutoPlay()
  }
})

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
  // ถ้าอยู่ในโหมด auto-play ให้หยุดการคลิกของผู้ใช้
  if (isAutoPlayActive.value) {
    console.log('Auto-play is active, ignoring user clicks')
    return
  }
  
  // ถ้าเป็น PvP หรือ Prompt Mode ให้ทั้ง X และ O เล่นได้
  if (!isPvP.value && !isPromptMode.value && currentPlayer.value !== 'X') return
  
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
        timeUsed: timeUsedSec
      })
      
      // สะสมเวลาที่ใช้
      if (currentPlayer.value === 'X') {
        xTotalTime.value += timeUsedSec
      } else {
        oTotalTime.value += timeUsedSec
      }
      
      switchPlayer()
      if (!isPromptMode.value) { // Only analyze strategy if not in prompt mode
        analyzeStrategyIfNeeded();
      }
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
  const directions = [
    [0, 1],  // ขวา
    [1, 0],  // ล่าง
    [0, -1], // ซ้าย
    [-1, 0], // บน
  ]

  const currentPiece = currentPlayer.value
  const enemy = currentPiece === 'X' ? 'O' : 'X'
  let capturedSet = new Set() // ใช้ Set เพื่อป้องกันการนับซ้ำ

  for (const [dr, dc] of directions) {
    // --- รูปแบบที่ 1: เดินเข้าไปตรงกลางระหว่างศัตรู 2 ตัว (Sandwich capture) ---
    const r1 = row - dr, c1 = col - dc
    const r2 = row + dr, c2 = col + dc
    
    if (
      inBounds(r1, c1) && inBounds(r2, c2) &&
      board.value[r1][c1] === enemy &&
      board.value[r2][c2] === enemy
    ) {
      capturedSet.add(`${r1},${c1}`)
      capturedSet.add(`${r2},${c2}`)
    }
    
    // --- รูปแบบที่ 2: หนีบศัตรูหลายตัวระหว่างหมากเรา 2 ตัว (Line capture) ---
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
      board.value[r][c] === currentPiece
    ) {
      for (const [cr, cc] of toCapture) {
        capturedSet.add(`${cr},${cc}`)
      }
    }
  }

  // ลบหมากที่ถูกกินออกจากกระดาน
  let capturedCount = 0
  for (const pos of capturedSet) {
    const [r, c] = pos.split(',').map(Number)
    board.value[r][c] = ''
    capturedCount++
  }

  // เพิ่มคะแนนให้ฝั่งที่เดิน
  if (capturedCount > 0) {
    if (currentPlayer.value === 'X') {
      xScore.value += capturedCount
    } else {
      oScore.value += capturedCount
    }
    checkGameEnd()
  }
}

function switchPlayer() {
  currentPlayer.value = currentPlayer.value === 'X' ? 'O' : 'X'
  turnStartTime.value = timeLeft.value // บันทึกเวลาตอนเริ่มเทิร์นใหม่

  // ถ้าไม่ใช่ PvP ให้ AI เดิน (รวมถึง Prompt Mode)
  if (!isPvP.value && currentPlayer.value === 'O') {
    console.log('🤖 AI turn detected!')
    console.log('isPromptMode:', isPromptMode.value)
    console.log('isAutoPlayActive:', isAutoPlayActive.value)
    
    if (isPromptMode.value && !isAutoPlayActive.value) {
      // ในโหมด prompt แต่ไม่ได้อยู่ในโหมด auto-play ให้เรียก AI เดินปกติ
      console.log('🎯 Calling AI move in prompt mode (manual play)')
      requestAIMove()
    } else if (!isPromptMode.value) {
      // โหมดปกติ (easy, medium, hard)
      console.log('🎯 Calling AI move in normal mode')
      requestAIMove()
    }
  }
  
  // ถ้าเป็น Prompt Mode และอยู่ในโหมด auto-play
  if (isPromptMode.value && isAutoPlayActive.value) {
    setTimeout(() => {
      executeAutoPlayMove()
    }, 1000) // หน่วงเวลา 1 วินาทีก่อนเดินตัวถัดไป
  }
}

const llmPlanActions = ref([]) // เก็บ action id ที่ LLM วางแผนไว้
const llmPlanStrategy = ref('') // เก็บชื่อกลยุทธ์ล่าสุดที่ LLM วางแผน

// ============ PROMPT MODE FUNCTIONS ============

function decodeActionId(action) {
  // action id = from_row * (8*8*8) + from_col * (8*8) + to_row * 8 + to_col
  const from_row = Math.floor(action / (8*8*8));
  let rem = action % (8*8*8);
  const from_col = Math.floor(rem / (8*8));
  rem = rem % (8*8);
  const to_row = Math.floor(rem / 8);
  const to_col = rem % 8;
  return [[from_row, from_col], [to_row, to_col]];
}

function findPieceForMove(targetFromRow, targetFromCol, targetToRow, targetToCol, player) {
  console.log(`🔍 findPieceForMove called for player ${player}`)
  console.log(`Target: (${targetFromRow},${targetFromCol}) → (${targetToRow},${targetToCol})`)
  
  // หาหมากที่ใกล้เคียงที่สุดกับตำแหน่งเป้าหมาย
  const pieceSymbol = player === 'X' ? 'X' : 'O'
  let bestPiece = null
  let bestDistance = Infinity
  
  console.log(`Looking for pieces: ${pieceSymbol}`)
  
  // ค้นหาหมากทั้งหมดของผู้เล่น
  for (let r = 0; r < 8; r++) {
    for (let c = 0; c < 8; c++) {
      if (board.value[r][c] === pieceSymbol) {
        console.log(`Found piece at (${r},${c})`)
        
        // คำนวณระยะห่างจากตำแหน่งเป้าหมาย
        const distance = Math.abs(r - targetFromRow) + Math.abs(c - targetFromCol)
        
        if (distance < bestDistance) {
          // ตรวจสอบว่าสามารถเดินไปยังตำแหน่งเป้าหมายได้หรือไม่
          if (isStraightMove(r, c, targetToRow, targetToCol) && 
              isPathClear(r, c, targetToRow, targetToCol) &&
              board.value[targetToRow][targetToCol] === '') {
            console.log(`✅ Valid move found: (${r},${c}) → (${targetToRow},${targetToCol})`)
            bestDistance = distance
            bestPiece = { from: [r, c], to: [targetToRow, targetToCol] }
          } else {
            // ถ้าเดินไม่ได้ตรงเป้าหมาย ลองหาทิศทางที่คล้ายกัน
            console.log(`❌ Direct move not possible, trying alternatives...`)
            const directions = [
              [0, 1], [0, -1], [1, 0], [-1, 0] // ขวา, ซ้าย, ลง, ขึ้น
            ]
            
            for (const [dr, dc] of directions) {
              for (let dist = 1; dist <= 3; dist++) {
                const newToRow = r + (dr * dist)
                const newToCol = c + (dc * dist)
                
                if (newToRow >= 0 && newToRow < 8 && newToCol >= 0 && newToCol < 8 &&
                    board.value[newToRow][newToCol] === '' &&
                    isStraightMove(r, c, newToRow, newToCol) &&
                    isPathClear(r, c, newToRow, newToCol)) {
                  
                  const altDistance = Math.abs(r - targetFromRow) + Math.abs(c - targetFromCol) + dist
                  if (altDistance < bestDistance) {
                    console.log(`✅ Alternative move found: (${r},${c}) → (${newToRow},${newToCol})`)
                    bestDistance = altDistance
                    bestPiece = { from: [r, c], to: [newToRow, newToCol] }
                  }
                  break
                }
              }
            }
          }
        }
      }
    }
  }
  
  console.log('Best piece found:', bestPiece)
  return bestPiece
}

async function executeAutoPlayMove() {
  console.log('🎯 executeAutoPlayMove called')
  console.log('isAutoPlayActive:', isAutoPlayActive.value)
  console.log('autoPlayTurnCount:', autoPlayTurnCount.value)
  console.log('maxAutoPlayTurns:', maxAutoPlayTurns.value)
  
  if (!isAutoPlayActive.value || autoPlayTurnCount.value >= maxAutoPlayTurns.value) {
    console.log('🛑 Stopping auto-play')
    stopAutoPlay()
    return
  }
  
  console.log(`Auto-play turn ${autoPlayTurnCount.value + 1}/${maxAutoPlayTurns.value} - Player: ${currentPlayer.value}`)
  
  let actionId = null
  let strategy = ''
  
  console.log('🎮 Getting action for player:', currentPlayer.value)
  
  if (currentPlayer.value === 'X') {
    // ผู้เล่น X ใช้กลยุทธ์ที่เลือก
    console.log('selectedStrategyActions:', selectedStrategyActions.value)
    console.log('actionIndex:', actionIndex.value)
    
    if (selectedStrategyActions.value.length > 0 && actionIndex.value < selectedStrategyActions.value.length) {
      actionId = selectedStrategyActions.value[actionIndex.value]
      strategy = selectedStrategy.value
      actionIndex.value++
      console.log('✅ Using strategy action:', actionId)
    } else {
      // ถ้าหมด actions ให้สุ่ม
      actionId = Math.floor(Math.random() * 4000) + 1
      strategy = selectedStrategy.value + ' (สุ่ม)'
      console.log('🎲 Using random action:', actionId)
    }
  } else {
    // ผู้เล่น O ใช้ LLM
    console.log('llmActions:', llmActions.value)
    console.log('llmActionIndex:', llmActionIndex.value)
    
    if (llmActions.value.length > 0 && llmActionIndex.value < llmActions.value.length) {
      actionId = llmActions.value[llmActionIndex.value]
      strategy = llmStrategy.value
      llmActionIndex.value++
      console.log('✅ Using LLM action:', actionId)
    } else {
      // ขอกลยุทธ์ใหม่จาก LLM
      console.log('🧠 Requesting new LLM strategy...')
      await requestLLMStrategy()
      if (llmActions.value.length > 0) {
        actionId = llmActions.value[0]
        strategy = llmStrategy.value
        llmActionIndex.value = 1
        console.log('✅ Got new LLM action:', actionId)
      } else {
        actionId = Math.floor(Math.random() * 4000) + 1
        strategy = 'LLM (สุ่ม)'
        console.log('🎲 Using random LLM action:', actionId)
      }
    }
  }
  
  // แปลง action ID เป็นตำแหน่ง
  console.log('🔍 Decoding action ID:', actionId)
  const [from, to] = decodeActionId(actionId)
  const [targetFromRow, targetFromCol] = from
  const [targetToRow, targetToCol] = to
  console.log('Target move:', { from, to })
  
  // หาหมากที่เหมาะสมสำหรับการเดิน
  console.log('🔍 Finding piece for move...')
  const move = findPieceForMove(targetFromRow, targetFromCol, targetToRow, targetToCol, currentPlayer.value)
  console.log('Found move:', move)
  
  if (move) {
    const [fromRow, fromCol] = move.from
    const [toRow, toCol] = move.to
    
    console.log(`✅ Executing move: ${fromRow},${fromCol} → ${toRow},${toCol}`)
    
    // ทำการเดินหมาก
    board.value[toRow][toCol] = board.value[fromRow][fromCol]
    board.value[fromRow][fromCol] = ''
    
    console.log('🎯 Move completed, updating history...')
    
    // บันทึกประวัติ
    const timeUsedSec = 1 // ใช้เวลา 1 วินาที
    moveHistory.value.push({
      turn: moveHistory.value.length + 1,
      player: currentPlayer.value,
      from: toChessPos(fromRow, fromCol),
      to: toChessPos(toRow, toCol),
      timeUsed: timeUsedSec,
      strategy: strategy,
      actionId: actionId
    })
    
    // ตรวจการกิน
    checkCapture(toRow, toCol)
    
    // เพิ่มจำนวนตา
    autoPlayTurnCount.value++
    
    // เพิ่มข้อมูลใน AI thoughts
    aiThoughtHistory.value.unshift({
      turn: moveHistory.value.length,
      player: currentPlayer.value,
      timestamp: new Date().toLocaleTimeString(),
      thoughts: `${currentPlayer.value === 'X' ? 'กลยุทธ์' : 'LLM'}: ${strategy} | Action ID: ${actionId} | เดิน ${toChessPos(fromRow, fromCol)} → ${toChessPos(toRow, toCol)}`,
      isProcessing: false
    })
    
    // สลับผู้เล่น
    console.log('🔄 Switching player...')
    switchPlayer()
  } else {
    console.log('❌ ไม่สามารถหาการเดินที่เหมาะสมได้')
    // ข้ามตานี้
    autoPlayTurnCount.value++
    console.log('⏭️ Skipping turn, switching player...')
    switchPlayer()
  }
}

async function requestLLMStrategy() {
  try {
    // เตรียมข้อมูลสำหรับส่งไป LLM แบบที่ backend คาดหวัง
    const gameHistory = moveHistory.value.map((m, idx) => 
      `[${idx + 1}] ${m.player}: ${m.from}→${m.to}`
    ).join('\n')
    
    const moveHistoryString = gameHistory || "เกมเพิ่งเริ่ม"
    
    console.log('📡 Sending to LLM:', moveHistoryString)
    
    try {
      const response = await axios.post('http://localhost:8000/hard-llm-plan', {
        board: getBoardState(),
        current_player: -1, // ฝั่ง AI (O)
        move_history: moveHistoryString
      })
      llmStrategy.value = response.data.strategy || 'กลยุทธ์ทั่วไป'
      llmActions.value = response.data.actions || []
      llmActionIndex.value = 0
      console.log('✅ LLM Response:', response.data)
    } catch (error) {
      console.log('⚠️ LLM API failed, using mock data:', error.message)
      
      // ใช้ mock data สำหรับ LLM
      const mockStrategies = ['ปิดฟ้าข้ามทะเล', 'ล้อมเวยช่วยจ้าว', 'ยืมดาบฆ่าคน', 'รอซ้ำยามเปลี้ย']
      const mockActions = [
        Math.floor(Math.random() * 4000) + 1,
        Math.floor(Math.random() * 4000) + 1,
        Math.floor(Math.random() * 4000) + 1,
        Math.floor(Math.random() * 4000) + 1,
        Math.floor(Math.random() * 4000) + 1
      ]
      
      llmStrategy.value = mockStrategies[Math.floor(Math.random() * mockStrategies.length)]
      llmActions.value = mockActions
      llmActionIndex.value = 0
      
      console.log('🎲 Using mock LLM data:', { strategy: llmStrategy.value, actions: llmActions.value })
    }
    
  } catch (error) {
    console.error('LLM Strategy request failed:', error)
    llmStrategy.value = 'กลยุทธ์ทั่วไป'
    llmActions.value = []
  }
}

function startAutoPlay(strategy, actions) {
  console.log('🎯 startAutoPlay called')
  console.log('Strategy:', strategy)
  console.log('Actions:', actions)
  
  selectedStrategy.value = strategy
  selectedStrategyActions.value = actions
  actionIndex.value = 0
  autoPlayTurnCount.value = 0
  isAutoPlayActive.value = true
  
  // รีเซ็ต LLM
  llmStrategy.value = ''
  llmActions.value = []
  llmActionIndex.value = 0
  
  console.log(`🚀 Auto-play started with strategy: ${strategy}`)
  console.log('isAutoPlayActive is now:', isAutoPlayActive.value)
  
  // เริ่มเดินทันที
  setTimeout(() => {
    console.log('⏰ Starting first auto-play move...')
    executeAutoPlayMove()
  }, 500)
}

function stopAutoPlay() {
  isAutoPlayActive.value = false
  autoPlayTurnCount.value = 0
  console.log('หยุด auto-play')
  
  // แสดงสรุปผล
  aiThoughtHistory.value.unshift({
    turn: moveHistory.value.length + 1,
    timestamp: new Date().toLocaleTimeString(),
    thoughts: `สรุปกลยุทธ์\n🏁 จบ Auto-play!\nกลยุทธ์ผู้เล่น: ${selectedStrategy.value}\nกลยุทธ์ Agent: ${llmStrategy.value}`,
    isProcessing: false
  })
}

async function requestAIMove() {
  if (difficulty.difficulty === 'hard') {
    // เรียก LLM เฉพาะเมื่อถึงรอบ 10, 20, 30, ...
    if ((moveHistory.value.length + 1) % 10 === 0) {
      // --- เตรียมข้อมูล situation ---
      const totalMoves = moveHistory.value.length;
      const player1Moves = moveHistory.value.filter(m => m.player === 'X').length;
      const player2Moves = moveHistory.value.filter(m => m.player === 'O').length;
      let horizontalMoves = 0;
      let verticalMoves = 0;
      let totalDistance = 0;
      moveHistory.value.forEach(m => {
        if (m.from && m.to) {
          const [fromRow, fromCol] = chessPosToRC(m.from);
          const [toRow, toCol] = chessPosToRC(m.to);
          if (fromRow === toRow) horizontalMoves++;
          if (fromCol === toCol) verticalMoves++;
          totalDistance += Math.abs(fromRow - toRow) + Math.abs(fromCol - toCol);
        }
      });
      const avgDistance = totalMoves > 0 ? (totalDistance / totalMoves) : 0;
      let situation = `สถานการณ์เกมหมากหนีบ:\n- จำนวนการเดินหมาก: ${totalMoves} ตา\n- ผู้เล่น 1: ${player1Moves} ตา, ผู้เล่น 2: ${player2Moves} ตา\n- การเดินแนวนอน: ${horizontalMoves} ตา\n- การเดินแนวตั้ง: ${verticalMoves} ตา\n- ระยะทางเฉลี่ย: ${avgDistance.toFixed(1)} ช่อง`;
      moveHistory.value.forEach((m, idx) => {
        const [fromRow, fromCol] = chessPosToRC(m.from);
        const [toRow, toCol] = chessPosToRC(m.to);
        const playerNum = m.player === 'X' ? 1 : -1;
        situation += `\nตาที่ ${idx + 1}: ผู้เล่น ${playerNum} เดิน (${fromRow},${fromCol}) → (${toRow},${toCol})`;
      });
      situation += '\nโปรดแนะนำกลยุทธ์ที่เหมาะสมจากสถานการณ์นี้';
      try {
        const res = await axios.post('http://localhost:8000/hard-llm-plan', {
          board: getBoardState(),
          current_player: -1, // ฝั่ง AI (O)
          move_history: situation
        });
        llmPlanActions.value = res.data.actions;
        llmPlanStrategy.value = res.data.strategy || '-';
        aiThoughtHistory.value.unshift({
          turn: moveHistory.value.length + 1,
          thoughts: `LLM เลือกกลยุทธ์: ${llmPlanStrategy.value}`,
          timestamp: new Date().toLocaleTimeString(),
          isPlanning: true
        });
      } catch (err) {
        console.error('AI move error:', err);
        llmPlanActions.value = [];
        llmPlanStrategy.value = '';
      }
    }
    // เดินตาม action id ถัดไปใน llmPlanActions (ถ้ามี)
    if (llmPlanActions.value.length > 0) {
      const action_id = llmPlanActions.value.shift();
      const [from, to] = decodeActionId(action_id);
      if (from && to) {
        const deltaRow = to[0] - from[0];
        const deltaCol = to[1] - from[1];
        let moved = false;
        outer: for (let r = 0; r < board.value.length; r++) {
          for (let c = 0; c < board.value[r].length; c++) {
            if (board.value[r][c] === 'O') {
              if ((deltaRow === 0 && deltaCol !== 0) || (deltaCol === 0 && deltaRow !== 0)) {
                const targetR = r + deltaRow;
                const targetC = c + deltaCol;
                if (inBounds(targetR, targetC) && board.value[targetR][targetC] === '' && isPathClear(r, c, targetR, targetC)) {
                  board.value[targetR][targetC] = 'O';
                  board.value[r][c] = '';
                  checkCapture(targetR, targetC);
                  moveHistory.value.push({
                    turn: moveHistory.value.length + 1,
                    player: 'O',
                    from: toChessPos(r, c),
                    to: toChessPos(targetR, targetC),
                    timeUsed: 0
                  });
                  aiThoughtHistory.value.unshift({
                    turn: aiThoughtHistory.value.length + 1,
                    thoughts: `AI (LLM) เดินจาก (${r},${c}) → (${targetR},${targetC}) (action id: ${action_id})`,
                    timestamp: new Date().toLocaleTimeString()
                  });
                  moved = true;
                  await sleep(500);
                  break outer;
                }
              }
            }
          }
        }
      }
      currentPlayer.value = 'X';
      return;
    } else {
      // ถ้าไม่มี action id ให้ fallback ไปใช้ AI เดิม
      try {
        const response = await axios.post('http://localhost:8000/ai-move', {
          board: getBoardState(),
          current_player: -1 // ฝั่ง AI (O)
        })
        const { from_row, from_col, to_row, to_col, action_id } = response.data
        board.value[to_row][to_col] = board.value[from_row][from_col]
        board.value[from_row][from_col] = ''
        checkCapture(to_row, to_col)
        aiThoughtHistory.value.unshift({
          turn: moveHistory.value.length + 1,
          thoughts: `AI (maknib_simulation) เดินจาก (${from_row},${from_col}) ไป (${to_row},${to_col}) [action_id: ${action_id}]`,
          timestamp: new Date().toLocaleTimeString()
        })
      } catch (err) {
        console.error('AI move error:', err)
      } finally {
        currentPlayer.value = 'X'
      }
      return;
    }
  }
  // ... โค้ดเดิมสำหรับ easy/medium/prompt ...
  try {
    const response = await axios.post('http://localhost:8000/ai-move', {
      board: getBoardState(),
      current_player: -1 // ฝั่ง AI (O)
    })
    const { from_row, from_col, to_row, to_col, action_id } = response.data
    board.value[to_row][to_col] = board.value[from_row][from_col]
    board.value[from_row][from_col] = ''
    checkCapture(to_row, to_col)
    
    // บันทึกการเดินลงในประวัติ
    const timeUsedSec = 1 // AI ใช้เวลา 1 วินาที
    moveHistory.value.push({
      turn: moveHistory.value.length + 1,
      player: 'O',
      from: toChessPos(from_row, from_col),
      to: toChessPos(to_row, to_col),
      timeUsed: timeUsedSec
    })
    
    // สะสมเวลาที่ใช้สำหรับ O
    oTotalTime.value += timeUsedSec
    
    aiThoughtHistory.value.unshift({
      turn: moveHistory.value.length,
      thoughts: `AI เลือกเดินจาก (${from_row},${from_col}) ไป (${to_row},${to_col}) [action_id: ${action_id}]`,
      timestamp: new Date().toLocaleTimeString()
    })
  } catch (err) {
    console.error('AI move error:', err)
  } finally {
    currentPlayer.value = 'X'
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
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

function restartGame() {
  // Reset game state
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

// ============ APPLY STRATEGY FUNCTION ============

async function applyStrategy(strategyIndex) {
  console.log('🚀 applyStrategy called with index:', strategyIndex)
  console.log('isAutoPlayActive:', isAutoPlayActive.value)
  
  if (isAutoPlayActive.value) {
    console.log('⚠️ Auto-play already active')
    alert('กำลังอยู่ในโหมด auto-play อยู่แล้ว')
    return
  }
  
  const strategy = filteredStrategies.value[strategyIndex]
  console.log('Selected strategy:', strategy)
  
  if (!strategy) {
    console.log('❌ Strategy not found')
    alert('ไม่พบกลยุทธ์ที่เลือก')
    return
  }
  
  try {
    console.log(`📡 Getting actions for strategy: ${strategy.name}`)
    
    // สร้าง mock actions ที่สมเหตุสมผลสำหรับกลยุทธ์แต่ละอัน
    const mockActionsByStrategy = {
      'ปิดฟ้าข้ามทะเล': [1234, 2345, 3456, 4567, 5678],
      'ล้อมเวยช่วยจ้าว': [1111, 2222, 3333, 4444, 5555],
      'ยืมดาบฆ่าคน': [1357, 2468, 3579, 4680, 5791],
      'รอซ้ำยามเปลี้ย': [1122, 3344, 5566, 7788, 9900],
      'ตีชิงตามไฟ': [1011, 1213, 1415, 1617, 1819],
      'ส่งเสียงบูรพาฝ่าตีประจิม': [2021, 2223, 2425, 2627, 2829],
      'มีในไม่มี': [3031, 3233, 3435, 3637, 3839],
      'ลอบตีเฉินชาง': [1000, 2000, 3000, 4000, 1500]
    }
    
    // หา actions สำหรับกลยุทธ์นี้หรือใช้ default
    let actions = mockActionsByStrategy[strategy.name] || []
    
    // ถ้าไม่มีในรายการ ให้สุ่ม actions
    if (actions.length === 0) {
      actions = Array.from({length: 5}, () => Math.floor(Math.random() * 4000) + 1)
    }
    
    console.log(`✅ Found ${actions.length} actions for strategy: ${strategy.name}`)
    console.log('Actions:', actions)
    
    // เริ่ม auto-play
    startAutoPlay(strategy.name, actions)
    
    // แสดงข้อความใน AI thoughts
    aiThoughtHistory.value.unshift({
      turn: moveHistory.value.length + 1,
      timestamp: new Date().toLocaleTimeString(),
      thoughts: `🚀 เริ่มใช้กลยุทธ์: ${strategy.name} | พบ ${actions.length} actions | จะเล่นฝั่งละ 5 รอบ`,
      isProcessing: false
    })
    
  } catch (error) {
    console.error('Apply strategy error:', error)
    alert('เกิดข้อผิดพลาดในการเรียกใช้กลยุทธ์')
  }
}

async function analyzeStrategyIfNeeded() {
  if (moveHistory.value.length > 0 && moveHistory.value.length % 10 === 0) {
    // --- สรุปข้อมูล ---
    const totalMoves = moveHistory.value.length;
    const player1Moves = moveHistory.value.filter(m => m.player === 'X').length;
    const player2Moves = moveHistory.value.filter(m => m.player === 'O').length;
    let horizontalMoves = 0;
    let verticalMoves = 0;
    let totalDistance = 0;
    // นับแนวนอน/แนวตั้ง และระยะทาง
    moveHistory.value.forEach(m => {
      if (m.from && m.to) {
        const [fromRow, fromCol] = chessPosToRC(m.from);
        const [toRow, toCol] = chessPosToRC(m.to);
        if (fromRow === toRow) horizontalMoves++;
        if (fromCol === toCol) verticalMoves++;
        totalDistance += Math.abs(fromRow - toRow) + Math.abs(fromCol - toCol);
      }
    });
    const avgDistance = totalMoves > 0 ? (totalDistance / totalMoves) : 0;
    // --- สร้างข้อความตาม format finetune ---
    let situation = `สถานการณ์เกมหมากหนีบ:\n- จำนวนการเดินหมาก: ${totalMoves} ตา\n- ผู้เล่น 1: ${player1Moves} ตา, ผู้เล่น 2: ${player2Moves} ตา\n- การเดินแนวนอน: ${horizontalMoves} ตา\n- การเดินแนวตั้ง: ${verticalMoves} ตา\n- ระยะทางเฉลี่ย: ${avgDistance.toFixed(1)} ช่อง`;
    // เพิ่มรายละเอียดการเดิน
    moveHistory.value.forEach((m, idx) => {
      const [fromRow, fromCol] = chessPosToRC(m.from);
      const [toRow, toCol] = chessPosToRC(m.to);
      const playerNum = m.player === 'X' ? 1 : -1;
      situation += `\nตาที่ ${idx + 1}: ผู้เล่น ${playerNum} เดิน (${fromRow},${fromCol}) → (${toRow},${toCol})`;
    });
    situation += '\nโปรดแนะนำกลยุทธ์ที่เหมาะสมจากสถานการณ์นี้';
    try {
      const res = await axios.post('http://localhost:8000/analyze-strategy', {
        move_history: situation
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

// helper function แปลง chess pos (เช่น 'a8') กลับเป็น row,col
function chessPosToRC(pos) {
  if (!pos || typeof pos !== 'string') return [0, 0];
  // pos เช่น 'a8' หรือ 'b3'
  const col = pos.charCodeAt(0) - 'a'.charCodeAt(0);
  const row = 8 - parseInt(pos[1]);
  return [row, col];
}

// เพิ่ม refs สำหรับกลยุทธ์
const selectedCategory = ref('all')
const strategySearch = ref('')

// กำหนดข้อมูลกลยุทธ์ทั้ง 36 รายการ
const allStrategies = ref([
  // กลยุทธ์ชนะศึก
  { name: "ปิดฟ้าข้ามทะเล", category: "กลยุทธ์ชนะศึก", description: "ทำให้ศัตรูสบายใจ คิดว่าไม่มีแผน แล้วโจมตีทันที" },
  { name: "ล้อมเวยช่วยจ้าว", category: "กลยุทธ์ชนะศึก", description: "บุกตีจุดสำคัญที่ศัตรูเผลอให้กำลังแตก" },
  { name: "ยืมดาบฆ่าคน", category: "กลยุทธ์ชนะศึก", description: "ใช้กำลังหรือทรัพยากรของคนอื่นแทนตัวเอง" },
  { name: "รอซ้ำยามเปลี้ย", category: "กลยุทธ์ชนะศึก", description: "รอให้ศัตรูเหนื่อยแล้วจึงลงมือ" },
  { name: "ตีชิงตามไฟ", category: "กลยุทธ์ชนะศึก", description: "ฉวยโอกาสตอนศัตรูกำลังวุ่นวาย" },
  { name: "ส่งเสียงบูรพาฝ่าตีประจิม", category: "กลยุทธ์ชนะศึก", description: "ล่อให้ศัตรูสนใจด้านหนึ่ง แล้วโจมตีอีกด้าน" },
  
  // กลยุทธ์เผชิญศึก
  { name: "มีในไม่มี", category: "กลยุทธ์เผชิญศึก", description: "สร้างเรื่องลวงให้ศัตรูสับสน" },
  { name: "ลอบตีเฉินชาง", category: "กลยุทธ์เผชิญศึก", description: "ทำทีจะเข้าทางหลัก แต่บุกทางลับ" },
  { name: "ดูไฟชายฝั่ง", category: "กลยุทธ์เผชิญศึก", description: "รอดูให้ศัตรูแตกกันเองก่อนค่อยลงมือ" },
  { name: "ซ่อนดาบในรอยยิ้ม", category: "กลยุทธ์เผชิญศึก", description: "แสร้งเป็นมิตร แล้วยิงทีหลัง" },
  { name: "หลี่ตายแทนถาว", category: "กลยุทธ์เผชิญศึก", description: "เสียของเล็กน้อยเพื่อได้กำไรใหญ่" },
  { name: "จูงแพะติดมือ", category: "กลยุทธ์เผชิญศึก", description: "ฉกเอาสิ่งเล็กๆ ตอนศัตรูไม่ทันระวัง" },
  
  // กลยุทธ์เข้าตี
  { name: "ตีหญ้าให้งูตื่น", category: "กลยุทธ์เข้าตี", description: "ส่งคนสอดแนมดูความเคลื่อนไหวก่อนบุก" },
  { name: "ยืมซากคืนชีพ", category: "กลยุทธ์เข้าตี", description: "ใช้สิ่งที่ยังพอใช้งานสร้างประโยชน์ใหม่" },
  { name: "ล่อเสือออกจากถ้ำ", category: "กลยุทธ์เข้าตี", description: "หลอกล่อให้ศัตรูหลุดจากป้อม แล้วบุก" },
  { name: "แสร้งปล่อยเพื่อจับ", category: "กลยุทธ์เข้าตี", description: "ปล่อยให้หนีแล้วไล่บี้จนอ่อนกำลัง" },
  { name: "โยนกระเบื้องล่อหยก", category: "กลยุทธ์เข้าตี", description: "ใช้สิ่งไม่สำคัญล่อให้หลง ยึดจริงทีหลัง" },
  { name: "จับโจรเอาหัวโจก", category: "กลยุทธ์เข้าตี", description: "มุ่งโจมตีผู้นำศัตรูให้ล่มทั้งกอง" },
  
  // กลยุทธ์ติดพัน
  { name: "ถอนฟืนใต้กระทะ", category: "กลยุทธ์ติดพัน", description: "ตัดกำลังใจศัตรูให้หมดแรงสู้" },
  { name: "กวนน้ำจับปลา", category: "กลยุทธ์ติดพัน", description: "ใช้อาการวุ่นวายของศัตรูให้เป็นประโยชน์" },
  { name: "จักจั่นลอกคราบ", category: "กลยุทธ์ติดพัน", description: "ทำเหมือนไม่ขยับ ก่อนเปลี่ยนแผนฉับพลัน" },
  { name: "ปิดประตูจับโจร", category: "กลยุทธ์ติดพัน", description: "ล้อมรอบจนศัตรูหนีไม่ได้" },
  { name: "คบไกลตีใกล้", category: "กลยุทธ์ติดพัน", description: "ผูกไมตรีกับที่ไกล แล้วตีที่ใกล้" },
  { name: "ยืมทางพรางกล", category: "กลยุทธ์ติดพัน", description: "ขอผ่านแล้วใช้เส้นทางโจมตี" },
  
  // กลยุทธ์ร่วมรบ
  { name: "ลักขื่อเปลี่ยนเสา", category: "กลยุทธ์ร่วมรบ", description: "สลับตำแหน่งสำคัญของศัตรู" },
  { name: "ชี้ต้นหม่อนด่าต้นไหว", category: "กลยุทธ์ร่วมรบ", description: "ขู่ให้ฝ่ายอื่นเกรงใจแทนเป้าหมายจริง" },
  { name: "แสร้งทำบอแต่ไม่บ้า", category: "กลยุทธ์ร่วมรบ", description: "ทำเป็นโง่ก่อนแล้วออกหมัดหนัก" },
  { name: "ขึ้นบ้านชักบันได", category: "กลยุทธ์ร่วมรบ", description: "ตัดหนทางถอยหลังเมื่อศัตรูเข้ามา" },
  { name: "ต้นไม้ผลิดอก", category: "กลยุทธ์ร่วมรบ", description: "เสริมกำลังเล็กให้ดูเข้มแข็ง" },
  { name: "สลับแขกเป็นเจ้าบ้าน", category: "กลยุทธ์ร่วมรบ", description: "เปลี่ยนฝ่ายให้ดูเหมือนเราเป็นเจ้าคุม" },
  
  // กลยุทธ์ยามพ่าย
  { name: "สาวงาม", category: "กลยุทธ์ยามพ่าย", description: "ใช้เสน่ห์หลอกใจศัตรูให้สับสน" },
  { name: "เปิดเมือง", category: "กลยุทธ์ยามพ่าย", description: "แสร้งอ่อนแอให้ศัตรูลังเลก่อนบุก" },
  { name: "ไส้ศึก", category: "กลยุทธ์ยามพ่าย", description: "ใช้คนในกองทัพศัตรูสร้างความแตกแยก" },
  { name: "ทุกข์กาย", category: "กลยุทธ์ยามพ่าย", description: "ทำตัวเจ็บเพื่อเรียกให้ศัตรูไว้ใจ" },
  { name: "ลูกโซ่", category: "กลยุทธ์ยามพ่าย", description: "ผูกแผนหลายขั้นให้ศัตรูตามไม่ทัน" },
  { name: "หลบหนี", category: "กลยุทธ์ยามพ่าย", description: "ถอยเพื่อรอเวลาที่ดีกว่า" },
])

// สร้าง computed properties สำหรับกรองข้อมูล
const filteredStrategies = computed(() => {
  let filtered = [...allStrategies.value]
  
  // กรองตามหมวดหมู่
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(strategy => strategy.category.includes(selectedCategory.value))
  }
  
  // กรองตามคำค้นหา
  if (strategySearch.value) {
    const searchLower = strategySearch.value.toLowerCase()
    filtered = filtered.filter(strategy => 
      strategy.name.toLowerCase().includes(searchLower) || 
      strategy.description.toLowerCase().includes(searchLower)
    )
  }
  
  return filtered
})

const showStrategyPanel = computed(() => !isPvP.value);
const showAIAnalysisPanel = computed(() => !isPvP.value);
const showApplyButton = computed(() => difficulty.difficulty === 'prompt');

const promptPlanActions = ref([]); // สำหรับโหมด prompt: action id ที่ต้องเดินตามกลยุทธ์
const promptPlanInProgress = ref(false); // true ขณะกำลังเดินตามกลยุทธ์
const promptPlanStep = ref(0); // นับจำนวนตาที่เดินไปแล้ว (สูงสุด 5)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap');

.game-container {
  font-family: 'Kanit', sans-serif;
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

/* Default layout for AI modes (Easy, Medium, Hard) */
.content {
  position: relative;
  z-index: 1;
  width: 100%;
  flex-grow: 1;
  display: grid;
  grid-template-columns: 350px 1fr; /* AI Panel left, Game Content right */
  gap: 2rem;
  padding: 2rem;
  transform: translateZ(0);
  min-height: calc(100vh - 4rem);
}

.ai-thoughts-panel {
  grid-column: 1 / 2; /* Explicitly place AI panel */
  height: 100%;
  background: linear-gradient(145deg, rgba(97, 26, 26, 0.95), rgba(10, 0, 0, 0.98));
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

.game-content {
  grid-column: 2 / 3; /* Explicitly place Game content */
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

/* Layout for PvP Mode */
.content.pvp-mode {
  grid-template-columns: 1fr; /* Game content takes full width */
}
.content.pvp-mode .game-content {
  grid-column: 1 / -1; /* Ensure it spans full width */
}

/* Layout for Prompt Mode */
.content.prompt-mode {
  grid-template-columns: 320px 1fr 320px;
  grid-template-areas: "ai-panel game-content prompt-panel";
  overflow: auto; /* เพิ่ม overflow: auto เพื่อให้สามารถเลื่อนได้ */
  max-height: 100vh; /* กำหนดความสูงสูงสุด */
}
.content.prompt-mode .ai-thoughts-panel,
.content.prompt-mode .game-content,
.content.prompt-mode .prompt-panel {
  height: auto;
  min-height: 80vh; /* ให้มีความสูงขั้นต่ำ */
  overflow-y: auto; /* ให้แต่ละส่วนสามารถเลื่อนได้เมื่อเนื้อหาเกิน */
}
.content.prompt-mode .game-content {
  display: flex;
  flex-direction: column;
}
.content.prompt-mode .game-board-container {
  flex: 1;
  min-height: 400px; /* กำหนดความสูงขั้นต่ำให้กระดาน */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.content.triple-panel {
  grid-template-columns: 350px 1fr 320px;
  grid-template-areas: "ai-panel game-content prompt-panel";
}
.content.triple-panel .ai-thoughts-panel {
  grid-column: 1 / 2;
}
.content.triple-panel .game-content {
  grid-column: 2 / 3;
}
.content.triple-panel .prompt-panel {
  grid-column: 3 / 4;
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

.thought-entry.processing {
  background: linear-gradient(135deg, rgba(0, 128, 0, 0.1), rgba(0, 100, 0, 0.05));
  border-color: rgba(0, 255, 0, 0.4);
  box-shadow: 0 0 15px rgba(0, 255, 0, 0.15);
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

/* ปรับแต่ง Prompt Panel ให้เหมือนกับในภาพ */
.prompt-panel {
  background: linear-gradient(145deg, rgba(23, 32, 68, 0.95), rgba(5, 10, 30, 0.98));
  padding: 1.5rem;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.prompt-panel .panel-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.2rem;
  padding-bottom: 0.8rem;
  border-bottom: 1px solid rgba(100, 149, 237, 0.2);
}

.prompt-icon {
  font-size: 1.8rem;
  margin-right: 0.8rem;
  color: #4caf50;
}

.panel-title {
  color: #4caf50;
  font-size: 1.4rem;
  margin: 0;
}

/* เพิ่ม CSS สำหรับแสดงรายการกลยุทธ์ */
.strategies-filter {
  display: flex;
  justify-content: space-between;
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.strategy-select {
  background: rgba(20, 30, 70, 0.7);
  border: 1px solid rgba(76, 175, 80, 0.4);
  color: white;
  padding: 0.5rem;
  border-radius: 6px;
  flex: 1;
}

.strategy-search {
  flex: 1;
}

.strategy-search-input {
  background: rgba(20, 30, 70, 0.7);
  border: 1px solid rgba(76, 175, 80, 0.4);
  color: white;
  padding: 0.5rem;
  border-radius: 6px;
  width: 100%;
}

.strategy-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.strategy-item {
  background: rgba(30, 40, 100, 0.4);
  border-radius: 16px;
  padding: 1rem;
  border-left: 3px solid #4caf50;
  transition: all 0.2s ease;
  position: relative;
  box-shadow: 0 10px 20px rgba(76, 175, 80, 0.08), 0 2px 8px rgba(0,0,0,0.08);
  border: 1px solid rgba(76, 175, 80, 0.13);
}

.strategy-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 0.8rem;
  width: 100%;
}

.strategy-title-container {
  display: flex;
  align-items: center;
}

/* สไตล์สำหรับปุ่มนำไปใช้ที่อยู่ด้านบนซ้าย */
.strategy-btn.top-left {
  background: #4caf4f24;
  color: #4caf50;
  border: 1px solid #4caf50;
  border-radius: 4px;
  padding: 0.25rem 0.7rem;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-right: auto; /* ให้ปุ่มอยู่ทางซ้ายสุด */
}

.strategy-btn.top-left:hover {
  background: #4caf50;
  transform: translateY(-1px);
}

/* ปรับความกว้างของหัวข้อให้พอดีกับพื้นที่ที่เหลือ */
.strategy-title {
  font-size: 1.1rem;
  color: #4caf50;
  margin: 0 0 0 0.5rem;
  flex-grow: 1;
}

.strategy-description {
  font-size: 0.85rem;
  color: #e0e0e0;
  line-height: 1.4;
  margin-bottom: 0.8rem;
}

.strategy-category {
  font-size: 0.75rem;
  color: #aaa;
  margin-bottom: 0.8rem;
  font-style: italic;
}

.strategy-btn {
  background: rgba(76, 175, 80, 0.2);
  color: #4caf50;
  border: 1px solid #4caf50;
  border-radius: 4px;
  padding: 0.3rem 0.8rem;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.strategy-btn:hover {
  background: rgba(76, 175, 80, 0.4);
}

/* สไตล์ scrollbar ของ strategy-list */
.strategy-list::-webkit-scrollbar {
  width: 6px;
}

.strategy-list::-webkit-scrollbar-track {
  background: rgba(76, 175, 80, 0.1);
  border-radius: 3px;
}

.strategy-list::-webkit-scrollbar-thumb {
  background: rgba(76, 175, 80, 0.3);
  border-radius: 3px;
}

.strategy-list::-webkit-scrollbar-thumb:hover {
  background: rgba(76, 175, 80, 0.5);
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

.board-header {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid rgba(255, 69, 0, 0.2);
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

/* Adjusted back-btn to flow with flexbox */
.back-btn {
  margin-top: auto; /* Pushes the button to the bottom within its flex container */
  background: linear-gradient(135deg, #ff6b6b, #dc143c);
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  padding: 0.8rem 1.5rem;
  border-radius: 50px;
  box-shadow: 0 4px 15px rgba(220, 20, 60, 0.3);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
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

.game-over-buttons .control-button {
  min-width: 160px;
  justify-content: center;
}

.game-over-buttons .back-btn {
  background: linear-gradient(135deg, #dc143c, #8b0000);
}

.game-over-buttons .replay-btn {
  background: linear-gradient(135deg, #4caf50, #2e7d32);
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

  .prompt-panel {
    padding: 1.5rem;
  }
} /* ปิด media query ที่ขาดหายไป */

@media (prefers-reduced-motion: reduce) {
  .fire-background,
  .ambient-particles,
  .difficulty-icon,
  .ai-icon,
  .thinking-animation,
  .board-glow,
  .possible-move,
  .move-dot,
  .prompt-icon {
    animation: none;
  }
  
  .cell,
  .piece,
  .control-button,
  .prompt-panel button {
    transition: none;
  }
}

/* Focus states for accessibility */
.control-button:focus,
.prompt-panel button:focus {
  outline: 3px solid rgba(255, 215, 0, 0.6);
  outline-offset: 2px;
}

/* เพิ่ม container สำหรับจัดวางหัวข้อและปุ่ม */
.header-container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
  margin-bottom: 1.5rem;
}

/* ปรับ difficulty-header ให้อยู่ซ้าย */
.difficulty-header {
  flex-grow: 1;
}

/* รีเซ็ต margin ของ difficulty-display */
.difficulty-display {
  margin-bottom: 0;
}

/* ปรับแต่งปุ่มกลับให้อยู่บนขวาสุด */
.back-btn.corner {
  position: absolute;
  top: 20px;
  right: 20px;
  margin: 0;
  font-size: 0.85rem;
  padding: 0.6rem 1.2rem;
  z-index: 10;
}

/* ปรับ game-content ให้มี position เป็น relative เพื่อรองรับ absolute positioning ของปุ่ม */
.game-content {
  position: relative;
  /* ...คงค่า properties อื่นไว้เหมือนเดิม... */
}

/* ปรับ header-container เพื่อไม่ให้ทับซ้อนกับปุ่ม */
.header-container {
  padding-top: 10px;
  padding-right: 100px; /* เพิ่มระยะห่างทางขวาเพื่อไม่ให้ชนกับปุ่ม */
}

/* Auto-play Status Styles */
.auto-play-status {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.status-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}

.status-icon {
  font-size: 1.2rem;
  animation: pulse 2s ease-in-out infinite;
}

.status-header h4 {
  color: white;
  margin: 0;
  font-size: 1rem;
  font-weight: 600;
}

.status-details {
  color: #ffffff;
  font-size: 0.85rem;
  line-height: 1.4;
  font-weight: 500;
}

.status-details p {
  margin: 0.2rem 0;
  color: #ffffff;
}

.stop-auto-play-btn {
  background: #ff4757;
  color: white;
  border: none;
  padding: 0.4rem 0.8rem;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  margin-top: 0.5rem;
  transition: all 0.3s ease;
}

.stop-auto-play-btn:hover {
  background: #ff3742;
  transform: translateY(-1px);
}

.strategy-btn:disabled {
  background: #95a5a6;
  cursor: not-allowed;
  opacity: 0.6;
}

.strategy-btn:disabled:hover {
  background: #95a5a6;
  transform: none;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* ปรับ responsive */
@media (max-width: 768px) {
  .back-btn.corner {
    top: 15px;
    right: 15px;
    font-size: 0.8rem;
    padding: 0.5rem 1rem;
  }
}

@media (max-width: 480px) {
  .back-btn.corner {
    top: 10px;
    right: 10px;
    padding: 0.4rem 0.8rem;
    font-size: 0.75rem;
  }
}
</style>