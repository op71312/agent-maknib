import os
from llama_cpp import Llama

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

def analyze_strategy_llm(move_history: str) -> str:
    llama = LLMStrategySingleton.get_llm()
    strategies_text = ", ".join(list_of_strategies)
    game_rules_summary = """กฎกติกาเกมหมากหนีบ:
* **วัตถุประสงค์:** ผู้เล่นแต่ละฝ่ายมีหมาก 8 ตัวบนกระดาน 8x8 วัตถุประสงค์คือการ \"หนีบ\" กินหมากฝ่ายตรงข้ามให้เหลือน้อยที่สุดหรือจนหมดเพื่อชนะ
* **การเดินหมาก:** เดินได้ครั้งละ 1 ตัว ในแนวตรง (ขึ้น-ลง-ซ้าย-ขวา) กี่ช่องก็ได้ ห้ามเดินเฉียงหรือข้ามหมาก
* **การหนีบ (จับกิน):**
    * **รูปแบบ 1:** ใช้หมากของเรา 1 ตัวอยู่ตรงกลางระหว่างหมากฝ่ายตรงข้าม 2 ตัวเพื่อกินหมาก 2 ตัวนั้น
    * **รูปแบบ 2:** ใช้หมากของเรา 2 ตัว \"หนีบ\" ล้อมรอบหมากฝ่ายตรงข้าม 1-2 ตัวเพื่อกินหมากที่ถูกหนีบ
* **เงื่อนไขการชนะ:** กินหมากฝ่ายตรงข้ามหมด หรือทำให้คู่แข่งเดินหมากไม่ได้ หรือมีหมากเหลือน้อยที่สุดเมื่อจบเกม หากเหลือหมากเท่ากันถือว่าเสมอ
"""
    instruction_with_input = f"""{game_rules_summary}

จากท่าเดินหมากที่กำหนดให้ จงวิเคราะห์และเลือกกลยุทธ์สามก๊กที่ตรงที่สุดจากรายการต่อไปนี้เท่านั้น:

{strategies_text}

ท่าเดินหมาก:
{move_history}

จงตอบในรูปแบบ:
กลยุทธ์: [ชื่อกลยุทธ์ที่คุณเลือก]
เหตุผล: [สรุปสั้นๆว่าท่าเดินหมากสอดคล้องกับกลยุทธ์ที่เลือกอย่างไร]"""

    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

### Instruction:
{}

### Input:

### Response:
{}"""
    full_prompt = alpaca_prompt.format(instruction_with_input, "")

    response = llama(
        prompt=full_prompt,
        max_tokens=130,
        stop=["###", "\n\n", '<', '>', '-', '\n\n\n'],
        echo=False,
        temperature=0.7,
        stream=False
    )
    # ถ้า response เป็น iterator ให้ใช้ next()
    if not isinstance(response, dict):
        response = next(response)
    return response['choices'][0]['text'].strip() 