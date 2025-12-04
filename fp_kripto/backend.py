# ================================
# backend.py — MD5 Suite Backend
# ================================

import hashlib
import pandas as pd
import time

# ================================
# Weak Password Database
# ================================
WEAK_HASH_DB = {
    "e10adc3949ba59abbe56e057f20f883e": "123456",
    "202cb962ac59075b964b07152d234b70": "123",
    "25d55ad283aa400af464c76d713c07ad": "12345678",
    "52c69e3a57331081823331c4e6999d23": "qwerty",
    "5f4dcc3b5aa765d61d8327deb882cf99": "password",
    "f33ba15effa5c10e873bf3842afb46a6": "iloveyou",
    "098f6bcd4621d373cade4e832627b4f6": "test",
}


# ================================
# Utility: Get File Size Safely
# ================================
def get_file_size(file_obj):
    pos = file_obj.tell()
    file_obj.seek(0, 2)
    size = file_obj.tell()
    file_obj.seek(pos)
    return size


# ================================
# MD5 Calculation
# ================================
def calculate_md5(file_obj):
    md5 = hashlib.md5()

    file_obj.seek(0)
    start = time.time()
    total_size = get_file_size(file_obj)

    for chunk in iter(lambda: file_obj.read(8192), b""):
        md5.update(chunk)

    end = time.time()
    file_obj.seek(0)

    size_mb = total_size / (1024 * 1024)
    duration = max(end - start, 0.0001)
    speed = size_mb / duration

    return md5.hexdigest(), speed


# ================================
# Batch Processor
# ================================
def process_batch(uploaded_files):
    rows = []

    for f in uploaded_files:
        md5, speed = calculate_md5(f)
        size_kb = round(get_file_size(f) / 1024, 2)

        rows.append({
            "Filename": f.name,
            "Size (KB)": size_kb,
            "MD5 Hash": md5,
            "Speed (MB/s)": round(speed, 2)
        })

    return pd.DataFrame(rows)


# ================================
# Weak Password Checker
# ================================
def check_weak_password(md5_hash):
    return WEAK_HASH_DB.get(md5_hash.lower())


# ================================
# VirusTotal Link
# ================================
def get_virustotal_link(md5_hash):
    return f"https://www.virustotal.com/gui/file/{md5_hash}"


# ================================
# Export CSV
# ================================
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")
