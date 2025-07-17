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