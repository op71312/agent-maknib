<template>
  <div class="game-container">
    <div class="fire-background"></div>
    <div class="ambient-particles"></div>
    
    <div class="content">
      <div class="rules-container">
        <div class="title-container">
          <h1 class="title">กติกาหมากหนีบ</h1>
          <div class="title-underline"></div>
        </div>
        
        <div class="rules-content">
          <div class="rule-section">
            <h3 class="section-title">
              <span class="section-icon">🎮</span>
              การตั้งหมาก
            </h3>
            <ul class="rule-list">
              <li>ใช้กระดานขนาด 8x8 ช่อง</li>
              <li>ผู้เล่นมี 2 ฝ่าย แต่ละฝ่ายมีหมาก 8 ตัว</li>
              <li>ฝ่ายแรก (⚫) วางหมากแถวล่างสุด</li>
              <li>ฝ่ายสอง (🔴) วางหมากแถวบนสุด</li>
            </ul>
          </div>

          <div class="rule-section">
            <h3 class="section-title">
              <span class="section-icon">🎯</span>
              วิธีเล่น
            </h3>
            <ul class="rule-list">
              <li>เดินสลับกันไปมาทีละฝ่าย ฝ่ายล่างเริ่มก่อน</li>
              <li>เดินได้แนวตรงเท่านั้น (แนวนอนหรือแนวตั้ง)</li>
              <li>เดินได้ไกลเท่าที่ต้องการ แต่ห้ามข้ามหมากตัวอื่น</li>
              <li>จับเวลาในการแข่งขัน 15นาที</li>
            </ul>
          </div>

          <div class="rule-section">
            <h3 class="section-title">
              <span class="section-icon">⚔️</span>
              การกินหมาก
            </h3>
            <p class="rule-description">กินได้ 3 แบบ:</p>
            
            <div class="examples-container">
              <div class="example-card">
                <h4 class="example-title">1. การกินแบบประกบ</h4>

                <div class="step-container">
                  <h5 class="step-title">ก่อนเดิน:</h5>
                  <div class="example-board">
                    <div class="board-row">
                      <div class="cell piece-black">⚫</div>
                      <div class="cell piece-red">🔴</div>
                      <div class="cell empty highlight">📍</div>
                    </div>
                  </div>
                  <div class="step-caption">หมาก ⚫ จะเดินไปตำแหน่ง 📍</div>
                </div>

                <div class="step-container">
                  <h5 class="step-title">หลังเดิน:</h5>
                  <div class="example-board">
                    <div class="board-row">
                      <div class="cell piece-black">⚫</div>
                      <div class="cell captured">❌</div>
                      <div class="cell piece-black new-piece">⚫</div>
                    </div>
                  </div>
                  <div class="step-caption">หมาก 🔴 ถูกประกบ → ถูกกิน!</div>
                </div>
              </div>

              <div class="example-card">
                <h4 class="example-title">2. การกินแบบเข้าไปแทรก</h4>

                <div class="step-container">
                  <h5 class="step-title">ก่อนเดิน:</h5>
                  <div class="example-board">
                    <div class="board-row">
                      <div class="cell piece-red">🔴</div>
                      <div class="cell empty highlight">📍</div>
                      <div class="cell piece-red">🔴</div>
                    </div>
                    <div class="board-row">
                      <div class="cell empty"></div>
                      <div class="cell piece-black">⚫</div>
                      <div class="cell empty"></div>
                    </div>
                  </div>
                  <div class="step-caption">หมาก ⚫ จะเดินไปแทรกตรงกลางตำแหน่ง 📍</div>
                </div>

                <div class="step-container">
                  <h5 class="step-title">หลังเดิน:</h5>
                  <div class="example-board">
                    <div class="board-row">
                      <div class="cell captured">❌</div>
                      <div class="cell piece-black new-piece">⚫</div>
                      <div class="cell captured">❌</div>
                    </div>
                    <div class="board-row">
                      <div class="cell empty"></div>
                      <div class="cell empty"></div>
                      <div class="cell empty"></div>
                    </div>
                  </div>
                  <div class="step-caption">หมาก 🔴 ทั้งสองตัวที่ขนาบถูกกิน! (+2 แต้ม)</div>
                </div>
              </div>

              <div class="example-card full-width">
                <h4 class="example-title">3. การกินหลายตัวพร้อมกัน</h4>
                
                <div class="step-container">
                  <h5 class="step-title">ก่อนเดิน:</h5>
                  <div class="example-board">
                    <div class="board-row">
                      <div class="cell piece-black">⚫</div>
                      <div class="cell piece-red">🔴</div>
                      <div class="cell piece-red">🔴</div>
                      <div class="cell empty highlight">📍</div>
                    </div>
                  </div>
                  <div class="step-caption">หมาก ⚫ จะเดินไปตำแหน่ง 📍 เพื่อประกบหมาก 🔴 ทั้งสองตัว</div>
                </div>

                <div class="step-container">
                  <h5 class="step-title">หลังเดิน:</h5>
                  <div class="example-board">
                    <div class="board-row">
                      <div class="cell piece-black">⚫</div>
                      <div class="cell captured">❌</div>
                      <div class="cell captured">❌</div>
                      <div class="cell piece-black new-piece">⚫</div>
                    </div>
                  </div>
                  <div class="step-caption">หมาก 🔴 ทั้งสองตัวถูกประกบ → ถูกกินทั้งคู่! (+2 แต้ม)</div>
                </div>
              </div>
            </div>
          </div>

          <div class="rule-section">
            <h3 class="section-title">
              <span class="section-icon">🏆</span>
              การชนะ-แพ้
            </h3>
            <ul class="rule-list">
              <li>ฝ่ายที่หมากถูกกินจนหมด หรือหมากเหลือน้อยกว่าจะเป็นฝ่ายแพ้</li>
              <li>ถ้าเล่นนจบครบ15นาทีแล้ว หมากทั้งสองฝ่ายเหลือเท่ากัน จะถือว่าเสมอ</li>
            </ul>
          </div>
        </div>
        
        <button @click="goBack" class="back-btn">
          <div class="btn-content">
            <i class="icon">🏠</i>
            <span>กลับหน้าหลัก</span>
          </div>
          <div class="btn-glow"></div>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

function goBack() {
  router.push('/')
}
</script>

<style scoped>

.game-container {
  font-family: 'Kanit', sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, #1a1a1a 0%, #000000 70%);
  overflow-y: auto;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 2rem 1rem;
  box-sizing: border-box;
}

.fire-background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 127, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(0, 191, 255, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(57, 255, 20, 0.2) 0%, transparent 50%),
    linear-gradient(45deg, 
      transparent 0%,
      rgba(0, 100, 100, 0.4) 25%,
      rgba(0, 255, 127, 0.3) 50%,
      rgba(0, 100, 100, 0.4) 75%,
      transparent 100%);
  background-size: 300% 300%, 250% 250%, 400% 400%, 200% 200%;
  animation: 
    fireEffect1 8s ease-in-out infinite,
    fireEffect2 12s ease-in-out infinite reverse,
    fireEffect3 15s ease-in-out infinite;
  z-index: 0;
}

.ambient-particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20px 30px, rgba(0, 255, 127, 0.8), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(0, 191, 255, 0.6), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(57, 255, 20, 0.5), transparent),
    radial-gradient(1px 1px at 130px 80px, rgba(0, 255, 127, 0.4), transparent),
    radial-gradient(2px 2px at 160px 30px, rgba(0, 191, 255, 0.3), transparent);
  background-repeat: repeat;
  background-size: 200px 100px;
  animation: sparkle 20s linear infinite;
  opacity: 0.6;
  z-index: 0;
}

.content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 900px;
  margin-top: 2rem;
}

.rules-container {
  background: linear-gradient(145deg, rgba(16, 72, 40, 0.95), rgba(19, 62, 40, 0.98));
  border-radius: 24px;
  padding: 4rem;
  box-shadow: 
    0 20px 40px rgba(0, 255, 127, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 127, 0.2);
  animation: slideUp 0.6s ease-out;
}

.title-container {
  text-align: center;
  margin-bottom: 3rem;
}

.title {
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 700;
  color: #fff;
  text-shadow: 
    0 0 10px rgba(0, 255, 127, 0.8),
    0 0 20px rgba(0, 255, 127, 0.6),
    0 0 30px rgba(0, 255, 127, 0.4);
  margin: 0;
  letter-spacing: 0.05em;
  animation: titleGlow 3s ease-in-out infinite;
}

.title-underline {
  width: 120px;
  height: 4px;
  background: linear-gradient(90deg, transparent, #00ff7f, #00bfff, #00ff7f, transparent);
  margin: 1.5rem auto 0;
  border-radius: 2px;
  animation: underlineGlow 2s ease-in-out infinite;
}

.rules-content {
  text-align: left;
  color: #e0ffe0;
  line-height: 1.9;
  font-size: 1.3rem;
}

.rule-section {
  margin-bottom: 3.5rem;
  padding: 3.5rem;
  background: linear-gradient(135deg, rgba(0, 255, 127, 0.08), rgba(0, 100, 100, 0.05));
  border-radius: 16px;
  border: 1px solid rgba(0, 255, 127, 0.15);
  transition: all 0.3s ease;
}

.rule-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 255, 127, 0.15);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1.2rem;
  color: #00ffff;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 2rem;
  text-shadow: 0 0 10px rgba(0, 255, 255, 0.5);
}

.section-icon {
  font-size: 2.5rem;
  animation: iconFloat 3s ease-in-out infinite;
}

.rule-description {
  color: #b3ffff;
  font-size: 1.7rem;
  margin-bottom: 2rem;
  font-weight: 500;
}

.rule-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.rule-list li {
  position: relative;
  padding: 1.5rem 0 1.5rem 3.5rem;
  margin-bottom: 1.2rem;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
  border-radius: 8px;
  border-left: 3px solid rgba(0, 255, 127, 0.5);
  transition: all 0.3s ease;
  font-size: 1.5rem;
}

.rule-list li:hover {
  background: linear-gradient(135deg, rgba(0, 255, 127, 0.1), rgba(0, 191, 255, 0.05));
  border-left-color: rgba(0, 255, 127, 0.8);
  transform: translateX(5px);
}

.rule-list li::before {
  content: '⚡';
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.4rem;
}

.examples-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 3rem;
  margin: 3rem 0;
}

.example-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border-radius: 16px;
  padding: 3.5rem;
  box-shadow: 
    0 8px 25px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(0, 255, 127, 0.2);
  transition: all 0.3s ease;
}

.example-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 15px 35px rgba(0, 255, 127, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.example-title {
  color: #ccff00;
  font-size: 1.9rem;
  font-weight: 600;
  margin-bottom: 2rem;
  text-align: center;
  text-shadow: 0 0 10px rgba(204, 255, 0, 0.5);
}

.example-board {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  margin: 2rem 0;
}

.board-row {
  display: flex;
  gap: 1rem;
}

.cell {
  width: 65px;
  height: 65px;
  border: 2px solid rgba(0, 255, 127, 0.4);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.2rem;
  position: relative;
  transition: all 0.3s ease;
}

.cell.empty {
  background: linear-gradient(145deg, #404040, #2a2a2a);
}

.cell.piece-black {
  background: linear-gradient(145deg, #2c3e50, #1a252f);
  border-color: #34495e;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
}

.cell.piece-red {
  background: linear-gradient(145deg, #e74c3c, #c0392b);
  border-color: #e67e22;
  box-shadow: 0 4px 8px rgba(231, 76, 60, 0.4);
}

.cell:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
}

.step-caption {
  text-align: center;
  font-size: 1.3rem;
  color: #b3ffff;
  font-weight: 500;
  line-height: 1.6;
  margin-top: 1.5rem;
  padding: 1.5rem;
  background: rgba(179, 255, 255, 0.08);
  border-radius: 8px;
  border: 1px solid rgba(179, 255, 255, 0.15);
}

.back-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.2rem;
  background: linear-gradient(135deg, #00ff7f 0%, #00cc66 100%);
  border: none;
  color: white;
  font-weight: 600;
  font-size: 1.6rem;
  padding: 1.8rem 3.5rem;
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 
    0 8px 25px rgba(0, 255, 127, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-family: 'Kanit', sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin: 3rem auto 0;
  overflow: hidden;
  min-width: 250px;
}

.btn-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 1.2rem;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #39ff14 0%, #00ff7f 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 50px;
}

.back-btn:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 
    0 15px 35px rgba(0, 255, 127, 0.5),
    0 5px 15px rgba(57, 255, 20, 0.4);
}

.back-btn:active {
  transform: translateY(-2px) scale(1.01);
}

.back-btn .icon {
  font-size: 1.8rem;
  transition: transform 0.3s ease;
}

.back-btn:hover .icon {
  transform: translateX(-3px);
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

@keyframes titleGlow {
  0%, 100% {
    text-shadow: 
      0 0 10px rgba(0, 255, 127, 0.8),
      0 0 20px rgba(0, 255, 127, 0.6),
      0 0 30px rgba(0, 255, 127, 0.4);
  }
  50% {
    text-shadow: 
      0 0 20px rgba(0, 255, 127, 1),
      0 0 30px rgba(0, 255, 127, 0.8),
      0 0 40px rgba(0, 255, 127, 0.6);
  }
}

@keyframes underlineGlow {
  0%, 100% {
    box-shadow: 0 0 10px rgba(0, 255, 127, 0.5);
    transform: scaleX(1);
  }
  50% {
    box-shadow: 0 0 20px rgba(0, 255, 127, 0.8);
    transform: scaleX(1.1);
  }
}

@keyframes iconFloat {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
}

@keyframes slideUp {
  from { 
    transform: translateY(50px); 
    opacity: 0; 
  }
  to { 
    transform: translateY(0); 
    opacity: 1; 
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .game-container {
    padding: 1rem;
  }
  
  .rules-container {
    padding: 2.5rem;
  }
  
  .content {
    margin-top: 1rem;
  }
  
  .examples-container {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .rule-section {
    padding: 2rem;
  }
  
  .section-title {
    font-size: 1.6rem;
  }
  
  .rule-description {
    font-size: 1.3rem;
  }
  
  .rule-list li {
    font-size: 1.2rem;
    padding: 1.2rem 0 1.2rem 3rem;
  }
  
  .rule-list li::before {
    left: 0.8rem;
    font-size: 1.1rem;
  }
  
  .example-card {
    padding: 2.5rem;
  }
  
  .example-title {
    font-size: 1.5rem;
  }
  
  .cell {
    width: 50px;
    height: 50px;
    font-size: 1.8rem;
  }
  
  .step-caption {
    font-size: 1rem;
    padding: 1.2rem;
  }
  
  .back-btn {
    padding: 1.2rem 2.5rem;
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .rules-container {
    padding: 2rem;
  }
  
  .rule-section {
    padding: 1.5rem;
  }
  
  .example-card {
    padding: 2rem;
  }
  
  .cell {
    width: 40px;
    height: 40px;
    font-size: 1.5rem;
  }
  
  .back-btn {
    padding: 1rem 2rem;
    font-size: 1.1rem;
    min-width: 180px;
  }
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .fire-background,
  .ambient-particles,
  .title,
  .title-underline,
  .section-icon {
    animation: none;
  }
  
  .back-btn,
  .rule-section,
  .example-card,
  .cell {
    transition: none;
  }
}

/* Focus states for accessibility */
.back-btn:focus {
  outline: 3px solid rgba(0, 255, 127, 0.6);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .rules-container {
    background: rgba(0, 0, 0, 0.9);
    border: 2px solid #fff;
  }
  
  .title {
    color: #fff;
    text-shadow: 2px 2px 4px #000;
  }
  
  .section-title {
    color: #fff;
    text-shadow: 1px 1px 2px #000;
  }
  
  .rule-list li {
    background: rgba(255, 255, 255, 0.1);
    border-left: 3px solid #fff;
  }
}

.full-width {
  grid-column: 1 / -1;
}

.step-container {
  margin: 1.5rem 0;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.03);
  border-radius: 12px;
  border: 1px solid rgba(0, 255, 127, 0.1);
}

.step-title {
  color: #ccff00;
  font-size: 1.6rem;
  font-weight: 600;
  margin-bottom: 1.2rem;
  text-align: center;
  text-shadow: 0 0 8px rgba(204, 255, 0, 0.4);
}

.cell.highlight {
  background: linear-gradient(145deg, #00ffff, #00bfff) !important;
  border-color: #0099cc !important;
  box-shadow: 0 0 15px rgba(0, 255, 255, 0.6) !important;
  animation: pulse 1.5s ease-in-out infinite;
}

.cell.possible-move {
  background: linear-gradient(145deg, #90ee90, #32cd32) !important;
  border-color: #228b22 !important;
  box-shadow: 0 0 10px rgba(50, 205, 50, 0.4) !important;
  font-size: 1rem;
  animation: glow 2s ease-in-out infinite;
}

.cell.captured {
  background: linear-gradient(145deg, #ff6b6b, #ff4444) !important;
  border-color: #cc0000 !important;
  box-shadow: 0 0 15px rgba(255, 0, 0, 0.5) !important;
  animation: fadeOut 0.8s ease-in-out;
}

.cell.new-piece {
  animation: slideIn 0.6s ease-out;
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.8) !important;
}

@keyframes pulse {
  0%, 100% { 
    transform: scale(1); 
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.6);
  }
  50% { 
    transform: scale(1.1); 
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.9);
  }
}

@keyframes glow {
  0%, 100% { 
    box-shadow: 0 0 10px rgba(50, 205, 50, 0.4);
  }
  50% { 
    box-shadow: 0 0 20px rgba(50, 205, 50, 0.8);
  }
}

@keyframes fadeOut {
  0% { 
    opacity: 1; 
    transform: scale(1);
  }
  100% { 
    opacity: 0.3; 
    transform: scale(0.8);
  }
}

@keyframes slideIn {
  0% { 
    transform: scale(0.5); 
    opacity: 0;
  }
  100% { 
    transform: scale(1); 
    opacity: 1;
  }
}

/* Responsive adjustments for new examples */
@media (max-width: 768px) {
  .step-container {
    padding: 0.8rem;
  }
  
  .step-caption {
    font-size: 0.85rem;
  }
}
</style>