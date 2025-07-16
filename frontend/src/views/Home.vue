<template>
  <div class="home-container">
    <div class="fire-background"></div>
    <div class="particles"></div>
    <div class="content">
      <div class="main-content">
        <div class="title-container">
          <h1 class="title">หมากหนีบ</h1>
          <div class="title-underline"></div>
        </div>
        <div class="game-options">
          <button class="game-button start-button" @click="startGame">
            <div class="button-content">
              <i class="play icon"></i>
              <span>เริ่มเกม</span>
            </div>
            <div class="button-glow"></div>
          </button>
          <button class="game-button rules-button" @click="showRules">
            <div class="button-content">
              <i class="book icon"></i>
              <span>กติกา</span>
            </div>
            <div class="button-glow"></div>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
  methods: {
    startGame() {
      this.$router.push('/level')
    },
    showRules() {
      this.$router.push('/rules');
    }
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;600;700&display=swap');

.home-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: radial-gradient(ellipse at center, #1a0000 0%, #000000 70%);
  overflow: hidden;
  font-family: 'Kanit', sans-serif;
}

.fire-background {
  position: absolute;
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
}

.particles {
  position: absolute;
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
}

.content {
  position: relative;
  z-index: 1;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.main-content {
  text-align: center;
  width: 90%;
  max-width: 800px;
  padding: 2rem;
}

.title-container {
  margin-bottom: 4rem;
  position: relative;
}

.title {
  font-size: clamp(3rem, 8vw, 8rem);
  font-weight: 700;
  color: #fff;
  text-shadow: 
    0 0 10px rgba(255, 69, 0, 0.8),
    0 0 20px rgba(255, 69, 0, 0.6),
    0 0 30px rgba(255, 69, 0, 0.4),
    0 0 40px rgba(255, 69, 0, 0.2);
  margin: 0;
  animation: glowText 3s ease-in-out infinite;
  letter-spacing: 0.1em;
  position: relative;
}

.title-underline {
  width: 100px;
  height: 4px;
  background: linear-gradient(90deg, transparent, #ff4500, #ff8c00, #ff4500, transparent);
  margin: 1rem auto;
  border-radius: 2px;
  animation: underlineGlow 2s ease-in-out infinite;
}

.game-options {
  display: flex;
  gap: 3rem;
  justify-content: center;
  flex-wrap: wrap;
}

.game-button {
  position: relative;
  padding: 1.5rem 3rem;
  border: none;
  border-radius: 15px;
  font-size: 1.4rem;
  font-weight: 600;
  font-family: 'Kanit', sans-serif;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  overflow: hidden;
  min-width: 200px;
}

.button-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
}

.button-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0;
  transition: opacity 0.3s ease;
  border-radius: 15px;
}

.start-button {
  background: linear-gradient(135deg, #dc143c 0%, #8b0000 100%);
  color: white;
  box-shadow: 
    0 8px 25px rgba(220, 20, 60, 0.3),
    inset 0 1px 0 rgba(255, 255, 255, 0.2);
}

.start-button .button-glow {
  background: linear-gradient(135deg, #ff1744 0%, #dc143c 100%);
}

.start-button:hover {
  transform: translateY(-8px) scale(1.05);
  box-shadow: 
    0 15px 35px rgba(220, 20, 60, 0.5),
    0 5px 15px rgba(255, 23, 68, 0.4);
}

.start-button:hover .button-glow {
  opacity: 1;
}

.rules-button {
  background: linear-gradient(135deg, #2c2c2c 0%, #1a1a1a 100%);
  color: white;
  box-shadow: 
    0 8px 25px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.1);
}

.rules-button .button-glow {
  background: linear-gradient(135deg, #404040 0%, #2c2c2c 100%);
}

.rules-button:hover {
  transform: translateY(-8px) scale(1.05);
  box-shadow: 
    0 15px 35px rgba(0, 0, 0, 0.6),
    0 5px 15px rgba(64, 64, 64, 0.4);
}

.rules-button:hover .button-glow {
  opacity: 1;
}

.game-button:active {
  transform: translateY(-4px) scale(1.02);
}

.game-button i {
  font-size: 1.6rem;
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
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(180deg); }
}

@keyframes glowText {
  0%, 100% {
    text-shadow: 
      0 0 10px rgba(255, 69, 0, 0.8),
      0 0 20px rgba(255, 69, 0, 0.6),
      0 0 30px rgba(255, 69, 0, 0.4),
      0 0 40px rgba(255, 69, 0, 0.2);
  }
  50% {
    text-shadow: 
      0 0 20px rgba(255, 69, 0, 1),
      0 0 30px rgba(255, 69, 0, 0.8),
      0 0 40px rgba(255, 69, 0, 0.6),
      0 0 50px rgba(255, 69, 0, 0.4);
  }
}

@keyframes underlineGlow {
  0%, 100% {
    box-shadow: 0 0 10px rgba(255, 69, 0, 0.5);
  }
  50% {
    box-shadow: 0 0 20px rgba(255, 69, 0, 0.8);
  }
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .title-container {
    margin-bottom: 3rem;
  }
  
  .game-options {
    flex-direction: column;
    gap: 2rem;
    align-items: center;
  }
  
  .game-button {
    width: 100%;
    max-width: 300px;
    padding: 1.2rem 2rem;
    font-size: 1.2rem;
  }
}

@media (max-width: 480px) {
  .game-button {
    padding: 1rem 1.5rem;
    font-size: 1.1rem;
    min-width: 180px;
  }
  
  .title-container {
    margin-bottom: 2.5rem;
  }
}

@media (prefers-reduced-motion: reduce) {
  .fire-background,
  .particles,
  .title,
  .title-underline {
    animation: none;
  }
  
  .game-button {
    transition: transform 0.2s ease;
  }
}

.game-button:focus {
  outline: 3px solid rgba(255, 69, 0, 0.6);
  outline-offset: 2px;
}
</style>
