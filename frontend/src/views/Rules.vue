<template>
  <div class="game-container">
    <!-- Fire background effects matching other pages -->
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
            </ul>
          </div>

          <div class="rule-section">
            <h3 class="section-title">
              <span class="section-icon">⚔️</span>
              การกินหมาก
            </h3>
            <p class="rule-description">กินได้ 2 แบบ:</p>
            
            <div class="examples-container">
              <!-- การกินแบบประกบ -->
              <div class="example-card">
                <h4 class="example-title">1. การกินแบบประกบ</h4>
                
                <!-- ก่อนเดิน -->
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

                <!-- หลังเดิน -->
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

              <!-- การกินแบบเข้าไปแทรก -->
              <div class="example-card">
                <h4 class="example-title">2. การกินแบบเข้าไปแทรก</h4>
                
                <!-- ก่อนเดิน -->
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

                <!-- หลังเดิน -->
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

              <!-- การกินหลายตัวพร้อมกัน -->
              <div class="example-card full-width">
                <h4 class="example-title">3. การกินหลายตัวพร้อมกัน</h4>
                
                <!-- ก่อนเดิน -->
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

                <!-- หลังเดิน -->
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
              <li>ถ้าเวลาหมดลงแล้วหมากทั้งสองฝ่ายเหลือเท่ากัน จะถือว่าเสมอ</li>
            </ul>
          </div>
        </div>
        
        <button @click="$router.push('/')" class="back-btn">
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

<script>
export default {
  name: 'Rules'
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap');

.game-container {
  font-family: 'Kanit', sans-serif;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: radial-gradient(ellipse at center, #1a0000 0%, #000000 70%);
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
    radial-gradient(circle at 20% 80%, rgba(255, 69, 0, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 140, 0, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(220, 20, 60, 0.2) 0%, transparent 50%),
    linear-gradient(45deg, 
      transparent 0%,
      rgba(139, 0, 0, 0.4) 25%,
      rgba(255, 69, 0, 0.3) 50%,
      rgba(139, 0, 0, 0.4) 75%,
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
    radial-gradient(2px 2px at 20px 30px, rgba(255, 69, 0, 0.8), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(255, 140, 0, 0.6), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(255, 215, 0, 0.5), transparent),
    radial-gradient(1px 1px at 130px 80px, rgba(255, 69, 0, 0.4), transparent),
    radial-gradient(2px 2px at 160px 30px, rgba(255, 140, 0, 0.3), transparent);
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
  background: linear-gradient(145deg, rgba(30, 0, 0, 0.95), rgba(10, 0, 0, 0.98));
  border-radius: 24px;
  padding: 3rem;
  box-shadow: 
    0 20px 40px rgba(255, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 69, 0, 0.2);
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
    0 0 10px rgba(255, 69, 0, 0.8),
    0 0 20px rgba(255, 69, 0, 0.6),
    0 0 30px rgba(255, 69, 0, 0.4);
  margin: 0;
  letter-spacing: 0.05em;
  animation: titleGlow 3s ease-in-out infinite;
}

.title-underline {
  width: 120px;
  height: 4px;
  background: linear-gradient(90deg, transparent, #ff4500, #ff8c00, #ff4500, transparent);
  margin: 1.5rem auto 0;
  border-radius: 2px;
  animation: underlineGlow 2s ease-in-out infinite;
}

.rules-content {
  text-align: left;
  color: #e8eaed;
  line-height: 1.8; /* เพิ่ม line-height เพื่อให้อ่านง่ายขึ้น */
  font-size: 1.2rem; /* เพิ่มขนาดตัวอักษรพื้นฐาน */
}

.rule-section {
  margin-bottom: 3rem;
  padding: 2.5rem; /* เพิ่ม padding */
  background: linear-gradient(135deg, rgba(255, 69, 0, 0.08), rgba(139, 0, 0, 0.05));
  border-radius: 16px;
  border: 1px solid rgba(255, 69, 0, 0.15);
  transition: all 0.3s ease;
}

.rule-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 69, 0, 0.15);
}

.section-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  color: #ff6b6b;
  font-size: 1.8rem; /* เพิ่มขนาดตัวอักษร */
  font-weight: 600;
  margin-bottom: 1.8rem; /* เพิ่ม margin */
  text-shadow: 0 0 10px rgba(255, 107, 107, 0.5);
}

.section-icon {
  font-size: 2.2rem; /* เพิ่มขนาดไอคอน */
  animation: iconFloat 3s ease-in-out infinite;
}

.rule-description {
  color: #ffb74d;
  font-size: 1.5rem; /* เพิ่มขนาดตัวอักษร */
  margin-bottom: 1.8rem; /* เพิ่ม margin */
  font-weight: 500;
}

.rule-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.rule-list li {
  position: relative;
  padding: 1.2rem 0 1.2rem 3rem; /* เพิ่ม padding */
  margin-bottom: 1rem; /* เพิ่มระยะห่าง */
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05), rgba(255, 255, 255, 0.02));
  border-radius: 8px;
  border-left: 3px solid rgba(255, 69, 0, 0.5);
  transition: all 0.3s ease;
  font-size: 1.3rem; /* เพิ่มขนาดตัวอักษร */
}

.rule-list li:hover {
  background: linear-gradient(135deg, rgba(255, 69, 0, 0.1), rgba(255, 140, 0, 0.05));
  border-left-color: rgba(255, 69, 0, 0.8);
  transform: translateX(5px);
}

.rule-list li::before {
  content: '🔥';
  position: absolute;
  left: 0.8rem; /* ปรับตำแหน่งไอคอน */
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.2rem; /* เพิ่มขนาดไอคอน */
}

.examples-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2.5rem; /* เพิ่ม gap */
  margin: 2.5rem 0; /* เพิ่ม margin */
}

.example-card {
  background: linear-gradient(145deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
  border-radius: 16px;
  padding: 2.5rem; /* เพิ่ม padding */
  box-shadow: 
    0 8px 25px rgba(0, 0, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 69, 0, 0.2);
  transition: all 0.3s ease;
}

.example-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 15px 35px rgba(255, 69, 0, 0.2),
    inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.example-title {
  color: #ffd700;
  font-size: 1.7rem; /* เพิ่มขนาดตัวอักษร */
  font-weight: 600;
  margin-bottom: 1.8rem; /* เพิ่ม margin */
  text-align: center;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.example-board {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem; /* เพิ่ม gap */
  margin: 1.8rem 0; /* เพิ่ม margin */
}

.board-row {
  display: flex;
  gap: 0.8rem; /* เพิ่ม gap */
}

.cell {
  width: 55px; /* เพิ่มขนาด cell */
  height: 55px; /* เพิ่มขนาด cell */
  border: 2px solid rgba(255, 69, 0, 0.4);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem; /* เพิ่มขนาดตัวอักษรใน cell */
  position: relative;
  transition: all 0.3s ease;
}

.cell.empty {
  background: linear-gradient(145deg, #f5deb3, #deb887);
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
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
}

.step-caption {
  text-align: center;
  font-size: 1.1rem; /* เพิ่มขนาดตัวอักษร */
  color: #ffb74d;
  font-weight: 500;
  line-height: 1.5; /* เพิ่ม line-height */
  margin-top: 1.2rem; /* เพิ่ม margin */
  padding: 1.2rem; /* เพิ่ม padding */
  background: rgba(255, 183, 77, 0.08);
  border-radius: 8px;
  border: 1px solid rgba(255, 183, 77, 0.15);
}

.back-btn {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  background: linear-gradient(135deg, #dc143c 0%, #8b0000 100%);
  border: none;
  color: white;
  font-weight: 600;
  font-size: 1.4rem; /* เพิ่มขนาดตัวอักษร */
  padding: 1.5rem 3rem; /* เพิ่ม padding */
  border-radius: 50px;
  cursor: pointer;
  box-shadow: 
    0 8px 25px rgba(220, 20, 60, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-family: 'Kanit', sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin: 2.5rem auto 0; /* เพิ่ม margin */
  overflow: hidden;
  min-width: 220px; /* เพิ่ม min-width */
}

.btn-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.btn-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #ff1744 0%, #dc143c 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 50px;
}

.back-btn:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 
    0 15px 35px rgba(220, 20, 60, 0.5),
    0 5px 15px rgba(255, 23, 68, 0.4);
}

.back-btn:hover .btn-glow {
  opacity: 1;
}

.back-btn:active {
  transform: translateY(-2px) scale(1.01);
}

.back-btn .icon {
  font-size: 1.6rem; /* เพิ่มขนาดไอคอน */
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
      0 0 10px rgba(255, 69, 0, 0.8),
      0 0 20px rgba(255, 69, 0, 0.6),
      0 0 30px rgba(255, 69, 0, 0.4);
  }
  50% {
    text-shadow: 
      0 0 20px rgba(255, 69, 0, 1),
      0 0 30px rgba(255, 69, 0, 0.8),
      0 0 40px rgba(255, 69, 0, 0.6);
  }
}

@keyframes underlineGlow {
  0%, 100% {
    box-shadow: 0 0 10px rgba(255, 69, 0, 0.5);
    transform: scaleX(1);
  }
  50% {
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.8);
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
    padding: 2rem;
  }
  
  .content {
    margin-top: 1rem;
  }
  
  .examples-container {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .rule-section {
    padding: 1.5rem;
  }
  
  .section-title {
    font-size: 1.5rem; /* ปรับลดขนาดสำหรับมือถือ */
  }
  
  .rule-description {
    font-size: 1.2rem; /* ปรับลดขนาดสำหรับมือถือ */
  }
  
  .rule-list li {
    font-size: 1.1rem; /* ปรับลดขนาดสำหรับมือถือ */
    padding: 1rem 0 1rem 2.5rem;
  }
  
  .rule-list li::before {
    left: 0.5rem;
    font-size: 1rem;
  }
  
  .example-card {
    padding: 2rem;
  }
  
  .example-title {
    font-size: 1.4rem; /* ปรับลดขนาดสำหรับมือถือ */
  }
  
  .cell {
    width: 45px;
    height: 45px;
    font-size: 1.5rem;
  }
  
  .step-caption {
    font-size: 0.95rem; /* ปรับลดขนาดสำหรับมือถือ */
    padding: 1rem;
  }
  
  .back-btn {
    padding: 1rem 2rem;
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .rules-container {
    padding: 1.5rem;
  }
  
  .rule-section {
    padding: 1rem;
  }
  
  .example-card {
    padding: 1.5rem;
  }
  
  .cell {
    width: 35px;
    height: 35px;
    font-size: 1.2rem;
  }
  
  .back-btn {
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
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
  outline: 3px solid rgba(255, 69, 0, 0.6);
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
  border: 1px solid rgba(255, 69, 0, 0.1);
}

.step-title {
  color: #ffd700;
  font-size: 1.4rem; /* เพิ่มขนาดตัวอักษร */
  font-weight: 600;
  margin-bottom: 1rem;
  text-align: center;
  text-shadow: 0 0 8px rgba(255, 215, 0, 0.4);
}

.step-caption {
  text-align: center;
  font-size: 1.1rem; /* เพิ่มขนาดตัวอักษร */
  color: #ffb74d;
  font-weight: 500;
  line-height: 1.5; /* เพิ่ม line-height */
  margin-top: 1.2rem; /* เพิ่ม margin */
  padding: 1.2rem; /* เพิ่ม padding */
  background: rgba(255, 183, 77, 0.08);
  border-radius: 8px;
  border: 1px solid rgba(255, 183, 77, 0.15);
}

.cell.highlight {
  background: linear-gradient(145deg, #ffd700, #ffb347) !important;
  border-color: #ff8c00 !important;
  box-shadow: 0 0 15px rgba(255, 215, 0, 0.6) !important;
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
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.8) !important;
}

@keyframes pulse {
  0%, 100% { 
    transform: scale(1); 
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
  }
  50% { 
    transform: scale(1.1); 
    box-shadow: 0 0 25px rgba(255, 215, 0, 0.9);
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