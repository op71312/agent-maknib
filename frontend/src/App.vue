<template>
  <router-view/>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap');

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Kanit', sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

:root {
  font-family: 'Kanit', sans-serif;
}

body {
  font-family: 'Kanit', sans-serif;
  line-height: 1.6;
}

/* ปรับ font-weight ให้บางลงเพื่อให้ดูไม่มีหัว */
h1, h2, h3, h4, h5, h6 {
  font-weight: 400;
}

button, input, select, textarea {
  font-family: 'Kanit', sans-serif;
}

.btn-title, .title, .section-title {
  font-weight: 400;
}

/* ปรับขนาดตัวอักษรให้ใหญ่ขึ้นเล็กน้อยเพื่อความอ่านง่าย */
body {
  font-size: 16px;
}

@media (max-width: 768px) {
  body {
    font-size: 14px;
  }
}
</style>
