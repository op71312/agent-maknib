<template>
  <div class="game-container">
    <div class="fire-background"></div>
    <div class="content">
      <transition name="fade">
        <div class="main-content">
          <h1 class="title">เลือกระดับความยาก</h1>
          <div class="level-options">
            <button class="ui massive level-btn easy" @click="selectLevel('easy')">
             
              ง่าย (Easy)
            </button>
            <button class="ui massive level-btn medium" @click="selectLevel('medium')">
              
              ปานกลาง (Medium)
            </button>
            <button class="ui massive level-btn hard" @click="selectLevel('hard')">
             
              ยาก (Hard)
            </button>
          </div>
          <button class="ui large back-button" @click="goBack">
            <i class="arrow left icon"></i>
            กลับ
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
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;600&display=swap');

.game-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #111;
  overflow: hidden;
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
    #880000 55%,
    transparent 100%
  );
  background-size: 200% 200%;
  animation: fireEffect 10s ease infinite;
  opacity: 0.5;
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

.game-content {
  max-width: 800px;
  width: 100%;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(12px);
  padding: min(5vw, 3rem);
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.title {
  font-size: 4rem;
  color: #fff;
  margin-bottom: 10rem;
  font-weight: 600;
  text-shadow: 0 0 10px #ff6a00;
}

.level-options {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 3.5rem;
  margin-bottom: 15rem;
}

.level-btn {
  position: relative;
  width: 300px;
  height: 140px;
  border-radius: 20px !important;
  color: #fff !important;
  font-size: 2rem !important;
  padding: 1rem 1.2rem !important;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  display: flex !important;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  text-align: left;
  font-weight: 600;
  overflow: hidden;
}

.level-btn::after {
  content: "🌱";
  position: absolute;
  top: 0px;
  right: 0px;
  background: rgba(255, 255, 255, 0.486);
  backdrop-filter: blur(5px);
  width: 40px;
  height: 40px;
  border-radius: 70%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
}

/* Emoji override per button */
.level-btn.medium::after {
  content: "⚡";
}
.level-btn.hard::after {
  content: "🔥";
}

.level-btn.easy {
  background: linear-gradient(135deg, #00c97c, #00b894) !important;
}

.level-btn.medium {
  background: linear-gradient(135deg, #ffb300, #ff6f00) !important;
}

.level-btn.hard {
  background: linear-gradient(135deg, #ff416c, #9932cc) !important;
}

.level-btn:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 24px rgba(255, 255, 255, 0.1);
}

.back-button {
  background: linear-gradient(90deg, #cc0000, #ff4444);
  border: none;
  color: white;
  font-weight: 700;
  font-size: 1.7rem;
  padding: 10px 28px;
  border-radius: 60px;
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
  0%, 100% {
    background-position: 0% 50%;
    opacity: 0.3;
  }
  50% {
    background-position: 100% 50%;
    opacity: 0.5;
  }
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }
  .level-options {
    flex-direction: column;
    align-items: center;
  }
  .level-btn {
    width: 90%;
  }
  
  .game-content {
    padding: 1.5rem;
  }
  
  .game-info {
    font-size: 0.9rem;
    padding: 0.8rem;
  }
}

@media (max-width: 480px) {
  .game-content {
    padding: 1rem;
  }
  
  .board {
    width: 95vw;
  }
}
</style>