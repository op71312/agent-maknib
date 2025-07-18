

---

# วิธีติดตั้งและรันโปรเจกต์ Agent Maknib (รวม backend, frontend, AI)

## โครงสร้างโปรเจกต์
```
agent-maknib/
  app/                # Python backend (FastAPI + AI)
  frontend/           # Vue.js frontend
  mak_nib_python/     # (optional) Python AI/เกม logic
  ...
```

## 1. เตรียมเครื่องมือพื้นฐาน
- Python 3.8+ (แนะนำ 3.10+)
- Node.js 16+ (แนะนำ 18+)
- npm (มากับ Node.js)
- git (ถ้ายังไม่มี)

## 2. ติดตั้ง Python Backend (FastAPI + AI)

### 2.1 สร้าง Python Virtual Environment
```bash
cd app
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 2.2 ติดตั้ง dependencies
> ถ้ามี requirements.txt:
```bash
pip install -r requirements.txt
```
> ถ้าไม่มี ให้ติดตั้งทีละตัว:
```bash
pip install fastapi uvicorn numpy torch pydantic llama-cpp-python
```

### 2.3 ตรวจสอบไฟล์โมเดล
- ไฟล์โมเดล AI: `app/ai/maknib_simulation.pth`
- ไฟล์ LLM: `app/llm/model/unsloth.Q4_K_M.gguf`

## 3. ติดตั้ง Frontend (Vue.js)
```bash
cd ../frontend
npm install
```

## 4. รัน Backend (FastAPI)
```bash
cd ../app
# (ถ้า venv ยังไม่ activate ให้ activate ก่อน)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- API จะรันที่ http://localhost:8000

## 5. รัน Frontend (Vue.js)
```bash
cd ../frontend
npm run dev
```
- เว็บจะรันที่ http://localhost:5173

## 6. (ถ้ามี) ติดตั้ง Python AI/เกม logic เพิ่มเติม
- ถ้าใช้ `mak_nib_python/` สำหรับรัน AI/เกม logic เพิ่มเติม ให้เข้าไปติดตั้ง dependencies ตามที่มีในโฟลเดอร์นั้น (ถ้ามี requirements.txt)

## 7. การใช้งาน
- เปิดเบราว์เซอร์ไปที่ http://localhost:5173
- เล่นเกมผ่าน UI ได้เลย
- Backend จะประมวลผล AI, LLM, กลยุทธ์ ฯลฯ

## 8. หมายเหตุ
- ถ้าใช้ GPU ให้ติดตั้ง torch เวอร์ชันที่รองรับ CUDA (`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`)
- ถ้า LLM ช้า ให้ตรวจสอบว่า llama-cpp-python รองรับ GPU หรือไม่
- ถ้าเจอปัญหาไฟล์โมเดลไม่เจอ ให้ตรวจสอบ path ให้ตรงกับที่โค้ดระบุ

## 9. TL;DR (สรุปคำสั่ง)
```bash
# Backend
cd app
python -m venv venv
venv\Scripts\activate  # หรือ source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd ../frontend
npm install
npm run dev
```
