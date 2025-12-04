import hashlib
import pandas as pd
import time
from io import BytesIO

# Database Password Lemah (Top 20 Common Passwords MD5)
WEAK_HASH_DB = {
    "e10adc3949ba59abbe56e057f20f883e": "123456",
    "202cb962ac59075b964b07152d234b70": "123",
    "25d55ad283aa400af464c76d713c07ad": "12345678",
    "52c69e3a57331081823331c4e6999d23": "qwerty",
    "5f4dcc3b5aa765d61d8327deb882cf99": "password",
    "f33ba15effa5c10e873bf3842afb46a6": "iloveyou",
    "098f6bcd4621d373cade4e832627b4f6": "test",
    # Bisa ditambahkan ribuan list lain di sistem nyata
}

def calculate_md5(file_obj):
    """Menghitung MD5 single file dengan chunking."""
    md5 = hashlib.md5()
    file_obj.seek(0)
    start_time = time.time()
    
    # Baca per 8KB
    for chunk in iter(lambda: file_obj.read(8192), b""):
        md5.update(chunk)
    
    end_time = time.time()
    file_obj.seek(0)
    
    # Hitung statistik
    file_size_mb = file_obj.size / (1024 * 1024)
    duration = end_time - start_time
    speed = file_size_mb / duration if duration > 0 else 0
    
    return md5.hexdigest(), speed

def process_batch(uploaded_files):
    """Memproses banyak file sekaligus."""
    results = []
    for f in uploaded_files:
        h, speed = calculate_md5(f)
        results.append({
            "Filename": f.name,
            "Size (KB)": round(f.size / 1024, 2),
            "MD5 Hash": h,
            "Speed (MB/s)": round(speed, 2)
        })
    return pd.DataFrame(results)

def check_weak_password(md5_hash):
    """Mengecek apakah hash ada di database password lemah."""
    return WEAK_HASH_DB.get(md5_hash, None)

def get_virustotal_link(md5_hash):
    """Generate link ke VirusTotal."""
    return f"https://www.virustotal.com/gui/file/{md5_hash}"

def convert_df_to_csv(df):
    """Convert DataFrame ke CSV untuk download."""
    return df.to_csv(index=False).encode('utf-8')