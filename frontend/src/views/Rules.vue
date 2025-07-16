<template>
  <div class="rules-container">
    <h2>กติกาหมากหนีบ</h2>
    <div class="rules-content">
      <h3>การตั้งหมาก</h3>
      <ul>
        <li>ใช้กระดานขนาด 8x8 ช่อง</li>
        <li>ผู้เล่นมี 2 ฝ่าย แต่ละฝ่ายมีหมาก 8 ตัว</li>
        <li>ฝ่ายแรก (X) วางหมากแถวบนสุด</li>
        <li>ฝ่ายสอง (O) วางหมากแถวล่างสุด</li>
      </ul>

      <h3>วิธีเล่น</h3>
      <ul>
        <li>เดินสลับกันไปมาทีละฝ่าย ฝ่ายบนเริ่มก่อน</li>
        <li>เดินได้แนวตรงเท่านั้น (แนวนอนหรือแนวตั้ง)</li>
        <li>เดินได้ไกลเท่าที่ต้องการ แต่ห้ามข้ามหมากตัวอื่น</li>
      </ul>

      <h3>การกินหมาก</h3>
      <ul>
        <li>กินได้ 2 แบบ:</li>
        <li>1. แบบประกบ: เดินหมากไปประกบหมากฝ่ายตรงข้ามที่อยู่ระหว่างหมากของเรา 2 ตัว</li>
        <li>2. แบบขนาบ: เดินหมากไปขนาบหมากฝ่ายตรงข้ามพร้อมกัน 2 ตัว</li>
        <li>สามารถกินหมากหลายตัวในตาเดียวกันได้</li>
      </ul>

      <h3>การชนะ-แพ้</h3>
      <ul>
        <li>ฝ่ายที่หมากถูกกินจนหมด หรือไม่มีทางเดินเหลือ เป็นฝ่ายแพ้</li>
        <li>ถ้าเล่นครบ 15 นาทีและคะแนนเท่ากันจะถือว่าเสมอ</li>
      </ul>
    </div>
    <button @click="$router.push('/')" class="back-btn">กลับหน้าหลัก</button>
  </div>
</template>

<script>
export default {
  name: 'Rules'
}
</script>

<style scoped>
.rules-container {
  max-width: 600px;
  margin: 3rem auto;
  background: #fff8f0;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(220,20,60,0.08);
  padding: 2.5rem;
  text-align: center;
  font-family: 'Kanit', sans-serif;
}
.rules-container h2 {
  color: #dc143c;
  margin-bottom: 1.5rem;
}
.rules-content {
  text-align: left;
  margin: 2rem 0;
}
.rules-content h3 {
  color: #8b0000;
  margin: 1.5rem 0 0.5rem 0;
}
.rules-content ul {
  margin-bottom: 1rem;
  padding-left: 1.5rem;
}
.rules-content li {
  margin: 0.5rem 0;
  line-height: 1.4;
}
.back-btn {
  background: linear-gradient(135deg, #dc143c 0%, #8b0000 100%);
  color: #fff;
  padding: 0.8rem 2rem;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(220,20,60,0.15);
  transition: background 0.3s;
}
.back-btn:hover {
  background: linear-gradient(135deg, #ff1744 0%, #dc143c 100%);
}
</style>