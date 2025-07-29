# วิธีใช้งาน ai_backend/main.py

## 1. ติดตั้ง `uv` (Python package manager ที่เร็วกว่า pip)

```sh
pip install uv
```

## 2. สร้างและเข้าใช้งาน virtual environment ด้วย `uv`

```sh
uv venv
.venv\Scripts\activate  # สำหรับ Windows
# หรือ
source .venv/bin/activate  # สำหรับ macOS/Linux
```

## 3. ติดตั้ง dependencies ที่จำเป็น

```sh
uv pip install torch numpy fastapi pydantic uvicorn
```

## 4. รัน FastAPI server

```sh
uvicorn app.main:app --reload
```

- API จะรันที่ http://127.0.0.1:8000
- สามารถทดสอบ endpoint ได้ที่ http://127.0.0.1:8000/docs

## 5. ออกจาก virtual environment

```sh
deactivate
```

---

**หมายเหตุ**
- หากต้องการใช้ GPU กับ PyTorch ให้ติดตั้ง torch เวอร์ชันที่รองรับ CUDA ตามคำแนะนำจาก https://pytorch.org/get-started/locally/
- หากพบปัญหา module not found ให้ตรวจสอบว่าได้ activate venv แล้วและติดตั้ง dependencies ใน venv นั้น

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
python -m venv env
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate
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
npm install -g vite  # ติดตั้ง vite CLI (ถ้ายังไม่มี)
npm install
```

## 4. รัน Backend (FastAPI)
```bash
cd ../app
# (ถ้า venv ยังไม่ activate ให้ activate ก่อน)
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- API จะรันที่ http://localhost:8000

## 5. รัน Frontend (Vue.js)
```bash
cd ../frontend
npm run dev
```
- เว็บจะรันที่ http://localhost:5173

## 6. การใช้งาน
- เปิดเบราว์เซอร์ไปที่ http://localhost:5173
- เล่นเกมผ่าน UI ได้เลย
- Backend จะประมวลผล AI, LLM, กลยุทธ์ ฯลฯ

## 7. หมายเหตุ
- ถ้าใช้ GPU ให้ติดตั้ง torch เวอร์ชันที่รองรับ CUDA (`pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`)
- ถ้า LLM ช้า ให้ตรวจสอบว่า llama-cpp-python รองรับ GPU หรือไม่
- ถ้าเจอปัญหาไฟล์โมเดลไม่เจอ ให้ตรวจสอบ path ให้ตรงกับที่โค้ดระบุ

## 8. TL;DR (สรุปคำสั่ง)
```bash
# Backend
cd app
python -m venv env
env\Scripts\activate  # หรือ source env/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd ../frontend
npm install -g vite
npm install
npm run dev
```

## 9. ติดต่อ/แจ้งปัญหา
- ถ้าติดปัญหาเรื่อง dependency, path, หรือ error ใด ๆ แจ้งรายละเอียดมาได้เลย!