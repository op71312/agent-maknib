import os
from llama_cpp import Llama
import unicodedata

class LLMStrategySingleton:
    _llm = None

    @classmethod
    def load_model(cls, model_path):
        if cls._llm is None:
            if not os.path.exists(model_path):
                raise ValueError(f"Model path does not exist: {model_path}")
            cls._llm = Llama(
                model_path=model_path,
                n_ctx=4096,
                n_threads=8,
                n_gpu_layers=-1,
                n_batch=512
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
    llama = LLMStrategySingleton.get_llm()
    # สร้าง situation แบบละเอียด
    situation = f"สถานการณ์เกมหมากหนีบ:\n{move_history}\n\nโปรดแนะนำกลยุทธ์ที่เหมาะสมจากสถานการณ์นี้"
    # system prompt ตามที่ใช้ finetune
    system_prompt = "คุณเป็นผู้เชี่ยวชาญการวิเคราะห์กลยุทธ์หมากหนีบ โปรดวิเคราะห์สถานการณ์การเดินหมากและแนะนำกลยุทธ์ที่เหมาะสม"
    # สร้าง prompt ตาม format ที่ใช้ train
    full_prompt = f"""<|im_start|>system\n{system_prompt}\n<|im_end|>\n<|im_start|>user\n{situation}\n<|im_end|>\n<|im_start|>assistant\n"""

    response = llama(
        prompt=full_prompt,
        max_tokens=130,
        stop=["<|im_end|>", "\n\n", "###", "\n"],
        echo=False,
        temperature=0.7,
        stream=False
    )
    if not isinstance(response, dict):
        response = next(response)
    return response['choices'][0]['text'].strip()

def analyze_strategy_and_plan_llm(move_history: str, board: list, current_player: int) -> dict:
    llama = LLMStrategySingleton.get_llm()
    situation = f"สถานการณ์เกมหมากหนีบ:\n{move_history}\n\nกระดานปัจจุบัน: {board}\nผู้เล่นที่กำลังเดิน: {current_player}\n\nโปรดวิเคราะห์กลยุทธ์ที่เหมาะสมและแนะนำ action id ที่ควรเดินต่อเนื่อง 10 ตา (action id ต้องไม่ผิดกติกาเกม)\nตัวอย่างรูปแบบคำตอบ:\nกลยุทธ์: [ชื่อกลยุทธ์]\nactions: [id1, id2, id3, ..., id10]"
    system_prompt = "คุณเป็นผู้เชี่ยวชาญการวิเคราะห์กลยุทธ์หมากหนีบ โปรดวิเคราะห์สถานการณ์และวางแผนการเดิน 10 ตาต่อไป (action id) ที่เหมาะสมและไม่ผิดกติกาเกม พร้อมระบุชื่อกลยุทธ์ที่เลือก"
    full_prompt = f"""<|im_start|>system\n{system_prompt}\n<|im_end|>\n<|im_start|>user\n{situation}\n<|im_end|>\n<|im_start|>assistant\n"""
    response = llama(
        prompt=full_prompt,
        max_tokens=256,
        stop=["<|im_end|>", "\n\n", "###", "\n"],
        echo=False,
        temperature=0.7,
        stream=False
    )
    if not isinstance(response, dict):
        response = next(response)
    text = response['choices'][0]['text'].strip()
    import re, ast
    strategy = None
    actions = []
    m = re.search(r'กลยุทธ์[:：]?\s*(.+)', text)
    if m:
        strategy = m.group(1).split('\n')[0].strip()
        strategy = normalize_strategy_name(strategy)
    m2 = re.search(r'actions?[:：]?\s*\[([^\]]+)\]', text)
    if m2:
        try:
            actions = [int(x) for x in m2.group(1).split(',') if x.strip().isdigit()]
        except Exception:
            actions = []
    return {'strategy': strategy, 'actions': actions, 'raw': text} 