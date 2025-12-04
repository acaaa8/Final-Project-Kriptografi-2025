import hashlib
import pandas as pd
import time
import os
import tarfile

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
# ROCKYOU CRACKER (VERSI .TAR.GZ FIX) 💀
# ================================
def check_rockyou(target_hash, wordlist_path="rockyou.txt"):
    target_hash = target_hash.strip().lower()
    
    # 1. Cek apakah file ada
    if not os.path.exists(wordlist_path):
        # Coba cek versi .tar.gz jika user lupa menulis ekstensi
        if os.path.exists(wordlist_path + ".tar.gz"):
            wordlist_path += ".tar.gz"
        else:
            return "ERROR_NO_FILE"

    tar_handle = None
    file_iterator = None

    try:
        # LOGIKA 1: Jika file kompresi (.tar.gz)
        if wordlist_path.endswith(".tar.gz"):
            tar_handle = tarfile.open(wordlist_path, "r:gz")
            
            # --- CARI FILE YANG BENAR (BUKAN FOLDER) ---
            target_member = None
            for member in tar_handle.getmembers():
                # Pastikan ini file, dan bukan file sampah metadata (._)
                if member.isfile() and not member.name.startswith("._") and "rockyou" in member.name:
                    target_member = member
                    break 
            
            # Jika filter nama 'rockyou' gagal, ambil file besar pertama
            if target_member is None:
                for member in tar_handle.getmembers():
                    if member.isfile() and member.size > 1000000:
                        target_member = member
                        break
            
            if target_member is None:
                return "ERROR: Arsip .tar.gz kosong atau rusak!"

            # Ekstrak file yang ditemukan
            file_iterator = tar_handle.extractfile(target_member)
        
        # LOGIKA 2: Jika file teks biasa (.txt)
        else:
            file_iterator = open(wordlist_path, "rb")

        # PROSES CRACKING
        found_password = None
        
        for line_bytes in file_iterator:
            try:
                # Decode latin-1 (standar rockyou)
                line_str = line_bytes.decode("latin-1").strip()
                
                # Cek Hash
                hashed_attempt = hashlib.md5(line_str.encode("utf-8")).hexdigest()
                
                if hashed_attempt == target_hash:
                    found_password = line_str
                    break # KETEMU!
            except:
                continue 

        # Tutup file
        if tar_handle: tar_handle.close()
        if file_iterator: file_iterator.close()

        return found_password

    except Exception as e:
        return f"ERROR SYSTEM: {str(e)}"

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