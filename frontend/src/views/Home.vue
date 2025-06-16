<template>
  <div class="home-container">
    <div class="fire-background"></div>
    <div class="content">
      <div class="main-content">
        <h1 class="title">หมากหนีบ</h1>
        <div class="game-options">
          <button class="ui massive red button" @click="startGame">
            <i class="play icon"></i>
            เริ่มเกม
          </button>
          <button class="ui massive black button" @click="showRules">
            <i class="book icon"></i>
            กติกา
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
      this.$router.push('/game');
    },
    showRules() {
      this.$router.push('/rules');
    }
  }
}
</script>

<style scoped>
.home-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #111;
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
    transparent 100%);
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
}

.main-content {
  text-align: center;
  width: 90%;
  max-width: 1200px;
}

.title {
  font-size: 6vw;
  color: #fff;
  text-shadow: 
    0 0 10px #ff0000,
    0 0 20px #ff0000,
    0 0 30px #ff0000;
  margin-bottom: 3rem;
  animation: glowText 2s ease-in-out infinite;
}

.game-options {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

.ui.button {
  transition: transform 0.3s, box-shadow 0.3s;
}

.ui.button:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(255, 0, 0, 0.4);
}

.ui.red.button {
  background-color: #aa0000 !important;
  color: white;
}

.ui.black.button {
  background-color: #222 !important;
  color: white;
}

@keyframes fireEffect {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

@keyframes glowText {
  0%, 100% {
    text-shadow: 
      0 0 10px #ff0000,
      0 0 20px #ff0000,
      0 0 30px #ff0000;
  }
  50% {
    text-shadow: 
      0 0 20px #ff0000,
      0 0 30px #ff0000,
      0 0 40px #ff0000;
  }
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .title {
    font-size: 9vw;
  }

  .game-options {
    flex-direction: column;
    gap: 1rem;
  }

  .ui.massive.button {
    font-size: 1rem !important;
    width: 100%;
  }
}
</style>
