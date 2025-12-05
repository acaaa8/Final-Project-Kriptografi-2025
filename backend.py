import hashlib
import pandas as pd
import time

# ================================
# Utility: Get File Size Safely
# ================================
def get_file_size(file_obj):
    try:
        pos = file_obj.tell()
        file_obj.seek(0, 2)
        size = file_obj.tell()
        file_obj.seek(pos)
        return size
    except:
        return 0

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

    # Hitung kecepatan proses
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
# VirusTotal Link Helper
# ================================
def get_virustotal_link(md5_hash):
    return f"https://www.virustotal.com/gui/file/{md5_hash}"

# ================================
# Export CSV
# ================================
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode("utf-8")