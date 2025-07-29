import os
from llama_cpp import Llama
import unicodedata
import hashlib
import threading
import time

# เพิ่ม Cache เพื่อความเร็ว
_strategy_cache = {}
_cache_lock = threading.Lock()

def get_cache_key(prompt: str) -> str:
    """สร้าง cache key จาก prompt"""
    return hashlib.md5(prompt.encode()).hexdigest()[:16]

def get_cached_response(prompt: str) -> str:
    """ดึงคำตอบจาก cache"""
    with _cache_lock:
        return _strategy_cache.get(get_cache_key(prompt))

def cache_response(prompt: str, response: str):
    """เก็บคำตอบใน cache"""
    with _cache_lock:
        _strategy_cache[get_cache_key(prompt)] = response
        # จำกัดขนาด cache ไม่เกิน 1000 entries
        if len(_strategy_cache) > 1000:
            # ลบ entry เก่าออก
            oldest_key = next(iter(_strategy_cache))
            del _strategy_cache[oldest_key]

class LLMStrategySingleton:
    _llm = None

    @classmethod
    def load_model(cls, model_path):
        if cls._llm is None:
            if not os.path.exists(model_path):
                raise ValueError(f"Model path does not exist: {model_path}")
            cls._llm = Llama(
                model_path=model_path,
                n_ctx=2048,  # ลดจาก 4096 เพื่อความเร็ว
                n_threads=16,  # เพิ่มจาก 8 เป็น 16
                n_gpu_layers=-1,  # ใช้ GPU ทั้งหมด
                n_batch=1024,  # เพิ่มจาก 512 เป็น 1024
                use_mlock=True,  # ป้องกัน swap memory
                use_mmap=True,   # ใช้ memory mapping
                flash_attn=True, # เปิด FlashAttention ถ้ามี
                rope_freq_base=10000.0,  # ปรับ RoPE สำหรับความเร็ว
                rope_freq_scale=1.0,
                tensor_split=None,  # Auto-split สำหรับ multi-GPU
                verbose=False    # ปิด verbose logs
            )
        return cls._llm

    @classmethod
    def get_llm(cls):
        if cls._llm is None:
            raise RuntimeError("LLM model not loaded! Call load_model() first.")
        return cls._llm

list_of_strategies = [
    'ปิดฟ้าข้ามทะเล', 'ล้อมเวยช่วยจ้าว', 'ยืมดาบฆ่าคน', 'รอซ้ำยามเปลี้ย',
    'ตีชิงตามไฟ', 'ส่งเสียงบูรพาฝ่าตีประจิม', 'มีในไม่มี', 'ลอบตีเฉินชาง',
    'ดูไฟชายฝั่ง', 'ซ่อนดาบในรอยยิ้ม', 'หลี่ตายแทนถาว', 'จูงแพะติดมือ',
    'ตีหญ้าให้งูตื่น', 'ยืมซากคืนชีพ', 'ล่อเสือออกจากถ้ำ', 'แสร้งปล่อยเพื่อจับ',
    'โยนกระเบื้องล่อหยก', 'จับโจรเอาหัวโจก', 'ถอนฟืนใต้กระทะ', 'กวนน้ำจับปลา',
    'จักจั่นลอกคราบ', 'ปิดประตูจับโจร', 'คบไกลตีใกล้', 'ยืมทางพรางกล',
    'ลักขื่อเปลี่ยนเสา', 'ชี้ต้นหม่อนด่าต้นไหว', 'แสร้งทำบอแต่ไม่บ้า', 'ขึ้นบ้านชักบันได',
    'ต้นไม้ผลิดอก', 'สลับแขกเป็นเจ้าบ้าน', 'สาวงาม', 'เปิดเมือง', 'ไส้ศึก', 'ทุกข์กาย', 'ลูกโซ่', 'หลบหนี'
]

def normalize_strategy_name(name):
    # ตัดช่องว่าง, lower, ตัดวรรณยุกต์
    def strip_accents(text):
        return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')
    name_norm = strip_accents(name.replace(' ', '').lower())
    best = None
    best_score = 0
    for s in list_of_strategies:
        s_norm = strip_accents(s.replace(' ', '').lower())
        # คะแนนความคล้าย (จำนวนตัวอักษรตรงกัน)
        score = sum(a == b for a, b in zip(name_norm, s_norm))
        if score > best_score:
            best_score = score
            best = s
    # ถ้าคะแนนน้อยมาก ให้คืนชื่อเดิม
    if best_score < 2:
        return name
    return best

def analyze_strategy_llm(move_history: str) -> str:
    # ตรวจสอบ cache ก่อน
    cache_key = get_cache_key(move_history[:500])
    cached = get_cached_response(cache_key)
    if cached:
        return cached
    
    llama = LLMStrategySingleton.get_llm()
    # ย่อ prompt ให้สั้นลง
    situation = f"สถานการณ์: {move_history[:500]}..."  # จำกัดความยาว
    system_prompt = "วิเคราะห์กลยุทธ์หมากหนีบ"  # ย่อ system prompt
    # ใช้ prompt แบบสั้น
    full_prompt = f"""<|im_start|>system\n{system_prompt}\n<|im_end|>\n<|im_start|>user\n{situation}\n<|im_end|>\n<|im_start|>assistant\n"""

    response = llama(
        prompt=full_prompt,
        max_tokens=64,  # ลดจาก 130 เป็น 64
        stop=["<|im_end|>", "\n\n"],  # ลด stop tokens
        echo=False,
        temperature=0.3,  # ลดจาก 0.7 เพื่อความเร็ว
        stream=False,
        repeat_penalty=1.1,  # ป้องกันการวนซ้ำ
        top_k=40,      # จำกัด sampling
        top_p=0.9      # nucleus sampling
    )
    if not isinstance(response, dict):
        response = next(response)
    
    result = response['choices'][0]['text'].strip()
    # เก็บผลลัพธ์ใน cache
    cache_response(cache_key, result)
    return result

def analyze_strategy_and_plan_llm(move_history: str, board: list, current_player: int) -> dict:
    # สร้าง cache key จากข้อมูลสำคัญ
    cache_input = f"{move_history[:200]}_{str(board)[:100]}_{current_player}"
    cache_key = get_cache_key(cache_input)
    cached = get_cached_response(cache_key)
    if cached:
        try:
            # แปลง cached string กลับเป็น dict
            import json
            return json.loads(cached)
        except:
            pass  # ถ้า parse ไม่ได้ให้ทำใหม่
    
    llama = LLMStrategySingleton.get_llm()
    # ย่อ prompt ให้สั้นลง
    situation = f"เกม: {move_history[:300]}...\nบอร์ด: {str(board)[:200]}...\nผู้เล่น: {current_player}\nต้องการ: กลยุทธ์และ 5 action ids"
    system_prompt = "วิเคราะห์กลยุทธ์หมากหนีบและแนะนำ action ids"
    full_prompt = f"""<|im_start|>system\n{system_prompt}\n<|im_end|>\n<|im_start|>user\n{situation}\n<|im_end|>\n<|im_start|>assistant\n"""
    
    response = llama(
        prompt=full_prompt,
        max_tokens=128,  # ลดจาก 256 เป็น 128
        stop=["<|im_end|>", "\n\n"],  # ลด stop tokens
        echo=False,
        temperature=0.3,  # ลดเพื่อความเร็ว
        stream=False,
        repeat_penalty=1.1,
        top_k=40,
        top_p=0.9
    )
    if not isinstance(response, dict):
        response = next(response)
    text = response['choices'][0]['text'].strip()
    
    import re, ast
    strategy = None
    actions = []
    
    # ย่อการ parse
    m = re.search(r'กลยุทธ์[:：]?\s*(.+)', text)
    if m:
        strategy = m.group(1).split('\n')[0].strip()
        strategy = normalize_strategy_name(strategy)
    
    m2 = re.search(r'actions?[:：]?\s*\[([^\]]+)\]', text)
    if m2:
        try:
            actions = [int(x) for x in m2.group(1).split(',')[:5] if x.strip().isdigit()]  # จำกัด 5 actions
        except Exception:
            actions = []
    
    result = {'strategy': strategy, 'actions': actions, 'raw': text}
    
    # เก็บผลลัพธ์ใน cache
    try:
        import json
        cache_response(cache_key, json.dumps(result))
    except:
        pass  # ถ้า serialize ไม่ได้ก็ข้าม
    
    return result 