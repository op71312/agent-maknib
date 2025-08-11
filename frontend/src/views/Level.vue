<template>
  <div class="game-container">
    <div class="fire-background"></div>
    <div class="ambient-particles"></div>
    
    <div class="content">
      <transition name="fade" appear>
        <div class="main-content">
          <div class="title-container">
            <h1 class="title">เลือกระดับความยาก</h1>
            <div class="title-underline"></div>
          </div>
          
          <div class="level-options">
            <button class="level-btn easy" @click="selectLevel('easy')">
              <div class="btn-content">
                <div class="btn-icon">🌱</div>
                <div class="btn-text">
                  <div class="btn-title">ง่าย</div>
                  <div class="btn-subtitle">Easy</div>
                </div>
              </div>
              <div class="btn-glow"></div>
            </button>
            
            <button class="level-btn medium" @click="selectLevel('medium')">
              <div class="btn-content">
                <div class="btn-icon">⚡</div>
                <div class="btn-text">
                  <div class="btn-title">ปานกลาง</div>
                  <div class="btn-subtitle">Medium</div>
                </div>
              </div>
              <div class="btn-glow"></div>
            </button>
            
            <button class="level-btn hard" @click="selectLevel('hard')">
              <div class="btn-content">
                <div class="btn-icon">🔥</div>
                <div class="btn-text">
                  <div class="btn-title">ยาก</div>
                  <div class="btn-subtitle">Hard</div>
                </div>
              </div>
              <div class="btn-glow"></div>
            </button>
            
            <button class="level-btn friend" @click="selectLevel('friend')">
              <div class="btn-content">
                <div class="btn-icon">🤝</div>
                <div class="btn-text">
                  <div class="btn-title">เล่นกับเพื่อน</div>
                  <div class="btn-subtitle">PvP Mode</div>
                </div>
              </div>
              <div class="btn-glow"></div>
            </button>
            
            <!-- เพิ่มโหมด Prompt -->
            <button class="level-btn prompt" @click="selectLevel('prompt')">
              <div class="btn-content">
                <div class="btn-icon">💬</div>
                <div class="btn-text">
                  <div class="btn-title">สั่งผ่าน Prompt</div>
                  <div class="btn-subtitle">Prompt Mode</div>
                </div>
              </div>
              <div class="btn-glow"></div>
            </button>
          </div>

          <button class="back-btn" @click="goBack" aria-label="กลับ">
            <div class="back-btn-icon">🏠</div>
            <span>กลับ</span>
          </button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Level',
  methods: {
    selectLevel(level) {
      this.$router.push({
        name: 'Game',
        params: { difficulty: level }
      })
    },
    goBack() {
      this.$router.push('/home')
    }
  }
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
  background: radial-gradient(ellipse at center, #1a1a1a 0%, #000000 70%);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
}

.fire-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 80%, rgba(0, 255, 127, 0.2) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(0, 191, 255, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(57, 255, 20, 0.1) 0%, transparent 50%),
    linear-gradient(45deg, 
      transparent 0%,
      rgba(0, 100, 100, 0.3) 25%,
      rgba(0, 255, 127, 0.2) 50%,
      rgba(0, 100, 100, 0.3) 75%,
      transparent 100%);
  background-size: 300% 300%, 250% 250%, 400% 400%, 200% 200%;
  animation: 
    fireEffect1 8s ease-in-out infinite,
    fireEffect2 12s ease-in-out infinite reverse,
    fireEffect3 15s ease-in-out infinite;
}

.ambient-particles {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: 
    radial-gradient(2px 2px at 20px 30px, rgba(0, 255, 127, 0.6), transparent),
    radial-gradient(2px 2px at 40px 70px, rgba(0, 191, 255, 0.5), transparent),
    radial-gradient(1px 1px at 90px 40px, rgba(57, 255, 20, 0.4), transparent),
    radial-gradient(1px 1px at 130px 80px, rgba(0, 255, 127, 0.3), transparent),
    radial-gradient(2px 2px at 160px 30px, rgba(0, 191, 255, 0.3), transparent);
  background-repeat: repeat;
  background-size: 200px 100px;
  animation: sparkle 20s linear infinite;
  opacity: 0.6;
}

/* ปรับ CSS ของปุ่ม "กลับ" */
.back-btn {
  display: flex;
  align-items: center;
  justify-content: center; /* จัดกึ่งกลางเมื่อเป็น flex */
  gap: 1rem;
  background: linear-gradient(135deg, #0080ff 0%, #004080 100%);
  border: none;
  color: white;
  font-weight: 650;
  font-size: 1.2rem;
  padding: 1.2rem 1.5rem;
  border-radius: 60px;
  cursor: pointer;
  box-shadow: 
    0 12px 35px rgba(0, 128, 255, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  font-family: 'Kanit', sans-serif;
  border: 1px solid rgba(255, 255, 255, 0.1);
  
  /* เพิ่ม margin เพื่อจัดตำแหน่งและระยะห่าง */
  margin-top: 3rem; /* ระยะห่างจากปุ่มเลือกระดับความยาก */
  margin-left: auto;
  margin-right: auto;
}

.back-btn-icon {
  font-size: 1.5rem; /* ปรับขนาดไอคอนให้เล็กลง */
  transition: transform 0.3s ease;
}

.back-btn:hover .back-btn-icon {
  transform: translateX(-3px);
}

.content {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
}

.main-content {
  text-align: center;
  width: 100%;
  max-width: 1400px; /* Reverted to original max-width */
  background: linear-gradient(145deg, rgba(20, 20, 20, 0.9), rgba(10, 10, 10, 0.95));
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 4rem 3rem; /* ปรับ padding หลัก */
  box-shadow: 
    0 20px 40px rgba(0, 255, 127, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(0, 255, 127, 0.3);
  overflow-y: auto; 
  max-height: 90vh; 
}

.title-container {
  margin-bottom: 4rem;
  position: relative;
}

.title {
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 700;
  color: #e0ffe0;
  text-shadow: 
    0 0 10px rgba(0, 255, 127, 0.8),
    0 0 20px rgba(0, 255, 127, 0.6),
    0 0 30px rgba(0, 255, 127, 0.4),
    0 0 40px rgba(0, 255, 127, 0.2);
  margin: 0;
  letter-spacing: 0.05em;
  animation: titleGlow 3s ease-in-out infinite;
}

.title-underline {
  width: 120px;
  height: 4px;
  background: linear-gradient(90deg, transparent, #00ff7f, #39ff14, #00ff7f, transparent);
  margin: 1.5rem auto 0;
  border-radius: 2px;
  animation: underlineGlow 2s ease-in-out infinite;
}

.level-options {
  display: flex; /* Changed from grid to flex */
  flex-wrap: wrap;
  justify-content: center; /* This will center the items, including the last row */
  gap: 2rem;
  max-width: 1200px; /* Reverted to original max-width */
  margin: 0 auto;
  margin-bottom: 3rem; 
}

.level-btn {
  position: relative;
  height: 180px;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  font-family: 'Kanit', sans-serif; 
  box-shadow: 
    0 10px 30px rgba(0, 0, 0, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.1);
  
  /* Flex basis for 3 columns */
  flex: 0 0 calc((100% - 4rem) / 3); /* (100% - 2 * gap) / 3 */
}

.btn-content {
  position: relative;
  z-index: 2;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  padding: 1.5rem; 
}

.btn-icon {
  font-size: 3rem;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3)); 
  animation: iconFloat 3s ease-in-out infinite; 
}

.btn-text {
  text-align: left;
}

.btn-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3); 
}

.btn-subtitle {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.8);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3); 
}

.btn-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 20px;
}

.level-btn.easy {
  background: linear-gradient(135deg, #00ff7f 0%, #00cc66 100%);
}

.level-btn.easy .btn-glow {
  background: linear-gradient(135deg, #39ff14 0%, #00ff7f 100%);
}

.level-btn.medium {
  background: linear-gradient(135deg, #00bfff 0%, #0080ff 100%);
}

.level-btn.medium .btn-glow {
  background: linear-gradient(135deg, #40e0ff 0%, #00bfff 100%);
}

.level-btn.hard {
  background: linear-gradient(135deg, #c0c0c0 0%, #808080 100%);
}

.level-btn.hard .btn-glow {
  background: linear-gradient(135deg, #e0e0e0 0%, #c0c0c0 100%);
}

.level-btn.friend {
  background: linear-gradient(135deg, #0066cc 0%, #003d7a 100%);
}

.level-btn.friend .btn-glow {
  background: linear-gradient(135deg, #0080ff 0%, #0066cc 100%);
}

.level-btn.prompt {
  background: linear-gradient(135deg, #00cccc 0%, #008080 100%);
}

.level-btn.prompt .btn-glow {
  background: linear-gradient(135deg, #40ffff 0%, #00cccc 100%);
}

.level-btn:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.4),
    0 0 30px rgba(0, 255, 127, 0.4);
}

.level-btn:hover .btn-glow {
  opacity: 1;
}

.level-btn:hover .btn-icon {
  transform: scale(1.1);
  animation-duration: 1s;
}

.level-btn:active {
  transform: translateY(-4px) scale(1.01);
}

/* Transitions */
.fade-enter-active, .fade-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(30px) scale(0.95);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-30px) scale(0.95);
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
      0 0 30px rgba(0, 255, 127, 0.4),
      0 0 40px rgba(0, 255, 127, 0.2);
  }
  50% {
    text-shadow: 
      0 0 20px rgba(0, 255, 127, 1),
      0 0 30px rgba(0, 255, 127, 0.8),
      0 0 40px rgba(0, 255, 127, 0.6),
      0 0 50px rgba(0, 255, 127, 0.4);
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

/* Responsive Design */
@media (max-width: 1400px) { /* สำหรับหน้าจอขนาดกลาง (2 คอลัมน์) */
  .level-options {
    max-width: 900px; /* Adjusted max-width for 2 columns */
  }
  .level-btn {
    flex: 0 0 calc((100% - 2rem) / 2); /* (100% - 1 * gap) / 2 */
  }
}

@media (max-width: 768px) { /* สำหรับหน้าจอขนาดเล็ก (1 คอลัมน์) */
  .back-btn {
    font-size: 1.1rem; 
    padding: 1rem 1.8rem; 
    border-radius: 50px;
  }
  .back-btn-icon {
    font-size: 1.4rem; 
  }
  
  .content {
    padding: 1rem;
  }
  
  .main-content {
    padding: 3.5rem 2.5rem; 
    max-height: 95vh; 
  }
  
  .level-options {
    max-width: 400px; /* Max width for 1 column */
  }
  .level-btn {
    flex: 0 0 100%; /* For 1 column */
  }
  
  .btn-content {
    gap: 1rem;
  }
  
  .btn-icon {
    font-size: 2.8rem; 
  }
  
  .btn-title {
    font-size: 1.6rem; 
  }
  
  .btn-subtitle {
    font-size: 0.95rem; 
  }
  
  .back-btn {
    padding: 0.9rem 1.6rem;
    font-size: 1rem;
    min-width: 160px;
  }
  .back-btn-icon {
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .main-content {
    padding: 2.5rem 1.5rem; 
  }
  
  .title-container {
    margin-bottom: 3rem;
  }
  
  .level-btn {
    height: 130px; 
  }
  
  .btn-content {
    flex-direction: column;
    gap: 0.5rem;
    text-align: center;
  }
  
  .btn-text {
    text-align: center;
  }
  
  .btn-icon {
    font-size: 2.2rem; 
  }
  
  .btn-title {
    font-size: 1.4rem; 
  }
  
  .btn-subtitle {
    font-size: 0.85rem; 
  }
  
  .back-btn {
    padding: 0.9rem 1.6rem;
    font-size: 1rem;
    min-width: 160px;
  }
  .back-btn-icon {
    font-size: 1.2rem;
  }
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  .fire-background,
  .ambient-particles,
  .title,
  .title-underline,
  .btn-icon {
    animation: none;
  }
  
  .level-btn,
  .back-btn {
    transition: none;
  }
}

/* Focus states for accessibility */
.level-btn:focus,
.back-btn:focus {
  outline: 3px solid rgba(255, 69, 0, 0.6);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .level-btn.easy {
    background: #00ff7f;
    border: 2px solid #fff;
  }
  
  .level-btn.medium {
    background: #00bfff;
    border: 2px solid #fff;
  }
  
  .level-btn.hard {
    background: #c0c0c0;
    border: 2px solid #fff;
  }
  
  .level-btn.friend {
    background: #0066cc;
    border: 2px solid #fff;
  }
  
  .level-btn.prompt {
    background: #00cccc;
    border: 2px solid #fff;
  }
  
  .title {
    color: #e0ffe0;
    text-shadow: 2px 2px 4px #000;
  }
}

/* Hover effects for desktop */
@media (hover: hover) {
  .level-btn:hover .btn-title {
    transform: translateX(5px);
    transition: transform 0.3s ease;
  }
  
  .level-btn:hover .btn-subtitle {
    transform: translateX(5px);
    transition: transform 0.3s ease 0.1s;
  }
}
</style>
