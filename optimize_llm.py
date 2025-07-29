#!/usr/bin/env python3
"""
สคริปต์สำหรับปรับแต่ง LLM ให้เร็วที่สุด
รันก่อนเริ่มเซิร์ฟเวอร์เพื่อ optimize performance
"""

import os
import psutil
import torch

def optimize_system_for_llm():
    """ปรับแต่งระบบเพื่อให้ LLM ทำงานเร็วที่สุด"""
    
    print("🚀 กำลังปรับแต่งระบบสำหรับ LLM...")
    
    # 1. ตั้งค่า environment variables สำหรับความเร็ว
    os.environ['OMP_NUM_THREADS'] = str(psutil.cpu_count())
    os.environ['MKL_NUM_THREADS'] = str(psutil.cpu_count())
    os.environ['OPENBLAS_NUM_THREADS'] = str(psutil.cpu_count())
    os.environ['VECLIB_MAXIMUM_THREADS'] = str(psutil.cpu_count())
    os.environ['NUMEXPR_NUM_THREADS'] = str(psutil.cpu_count())
    
    # 2. ปิด Python garbage collection ชั่วคราว (เพิ่มความเร็ว)
    import gc
    gc.disable()
    
    # 3. ตั้งค่า CUDA ถ้ามี
    if torch.cuda.is_available():
        os.environ['CUDA_LAUNCH_BLOCKING'] = '0'  # เปิด async execution
        torch.backends.cudnn.benchmark = True    # เพิ่มความเร็ว cudnn
        torch.backends.cudnn.deterministic = False
        print(f"✅ CUDA optimized: {torch.cuda.get_device_name()}")
    
    # 4. ตั้งค่า memory management
    try:
        import ctypes
        libc = ctypes.CDLL("libc.so.6")
        # ปิด malloc mmap threshold เพื่อประสิทธิภาพ
        libc.mallopt(1, 0)  # M_MXFAST
        print("✅ Memory optimization applied")
    except:
        pass
    
    print("✅ ระบบปรับแต่งเรียบร้อย!")

def get_optimal_llama_config():
    """คืนค่า config ที่เหมาะสมสำหรับระบบปัจจุบัน"""
    cpu_count = psutil.cpu_count()
    available_memory = psutil.virtual_memory().available // (1024**3)  # GB
    
    # ปรับ config ตาม hardware
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory // (1024**3)
        print(f"🔍 GPU Memory: {gpu_memory}GB")
        
        if gpu_memory >= 8:  # High-end GPU
            return {
                'n_ctx': 2048,
                'n_threads': min(16, cpu_count),
                'n_batch': 1024,
                'n_gpu_layers': -1,  # ใช้ GPU ทั้งหมด
                'use_mlock': True,
                'use_mmap': True,
                'rope_freq_base': 10000.0,
                'flash_attn': True
            }
        else:  # Mid-range GPU
            return {
                'n_ctx': 1536,
                'n_threads': min(12, cpu_count),
                'n_batch': 512,
                'n_gpu_layers': 20,  # บางส่วนใน GPU
                'use_mlock': True,
                'use_mmap': True
            }
    else:  # CPU only
        return {
            'n_ctx': 1024,
            'n_threads': cpu_count,
            'n_batch': 256,
            'n_gpu_layers': 0,
            'use_mlock': False,
            'use_mmap': True
        }

if __name__ == "__main__":
    optimize_system_for_llm()
    config = get_optimal_llama_config()
    print("📋 Optimal config:", config)
