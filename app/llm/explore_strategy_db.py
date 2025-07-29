# ─── สำรวจข้อมูลใน strategy_production.db ───
import sqlite3
import pandas as pd
import os

def explore_strategy_database(db_path):
    """สำรวจและแสดงข้อมูลในฐานข้อมูล SQLite"""
    
    if not os.path.exists(db_path):
        print(f"❌ ไม่พบไฟล์ฐานข้อมูล: {db_path}")
        return
    
    print(f"🔍 สำรวจฐานข้อมูล: {os.path.basename(db_path)}")
    print("="*60)
    
    try:
        # เชื่อมต่อฐานข้อมูล
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. แสดงรายชื่อตารางทั้งหมด
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"📊 จำนวนตาราง: {len(tables)}")
        print("📋 รายชื่อตาราง:")
        for i, (table_name,) in enumerate(tables, 1):
            print(f"   {i}. {table_name}")
        
        print("\n" + "="*60)
        
        # 2. สำรวจแต่ละตาราง
        for table_name, in tables:
            print(f"\n🔍 ตาราง: {table_name}")
            print("-" * 40)
            
            # ดูโครงสร้างตาราง
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = cursor.fetchall()
            
            print("📝 โครงสร้างคอลัมน์:")
            for col_info in columns_info:
                col_id, col_name, col_type, not_null, default_val, pk = col_info
                pk_text = " (PRIMARY KEY)" if pk else ""
                not_null_text = " NOT NULL" if not_null else ""
                default_text = f" DEFAULT {default_val}" if default_val else ""
                print(f"   • {col_name}: {col_type}{pk_text}{not_null_text}{default_text}")
            
            # นับจำนวนแถว
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
            print(f"\n📈 จำนวนแถว: {row_count:,}")
            
            if row_count > 0:
                # แสดงตัวอย่างข้อมูล 5 แถวแรก
                print(f"\n📋 ตัวอย่างข้อมูล 5 แถวแรก:")
                df_sample = pd.read_sql_query(f"SELECT * FROM {table_name} LIMIT 5", conn)
                print(df_sample.to_string(index=False))
                
                # แสดงข้อมูลเฉพาะคอลัมน์ที่น่าสนใจ
                if 'strategy' in [col.lower() for col in df_sample.columns]:
                    print(f"\n🎯 กลยุทธ์ที่แตกต่างกัน:")
                    unique_strategies = pd.read_sql_query(
                        f"SELECT DISTINCT strategy FROM {table_name} ORDER BY strategy", 
                        conn
                    )
                    for i, strategy in enumerate(unique_strategies['strategy'], 1):
                        print(f"   {i:2d}. {strategy}")
                
                # ถ้ามีคอลัมน์ action_sequence
                action_cols = [col for col in df_sample.columns if 'action' in col.lower()]
                if action_cols:
                    print(f"\n🎮 คอลัมน์ที่เกี่ยวข้องกับ Action:")
                    for col in action_cols:
                        print(f"   • {col}")
                        sample_value = df_sample[col].dropna().iloc[0] if not df_sample[col].dropna().empty else "N/A"
                        print(f"     ตัวอย่าง: {str(sample_value)[:100]}...")
            
            print("\n" + "-" * 40)
        
        # 3. สถิติรวม
        print(f"\n📊 สถิติรวมฐานข้อมูล:")
        total_rows = 0
        for table_name, in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            total_rows += count
            print(f"   • {table_name}: {count:,} แถว")
        
        print(f"\n📈 รวมทั้งหมด: {total_rows:,} แถว")
        
        # 4. ขนาดไฟล์
        file_size = os.path.getsize(db_path)
        size_mb = file_size / (1024 * 1024)
        print(f"💾 ขนาดไฟล์: {size_mb:.2f} MB ({file_size:,} bytes)")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    # กำหนด path ของฐานข้อมูล
    db_path = r"c:\university\nsc\agent-maknib\app\llm\strategy_production.db"
    
    # เริ่มสำรวจ
    explore_strategy_database(db_path)
