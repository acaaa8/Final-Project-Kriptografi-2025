import streamlit as st
import time
import pandas as pd
import hashlib
import requests  # Perlu install: pip install requests
import backend as bk  # Pastikan backend.py ada

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MD5 Ultimate Suite",
    page_icon="🛡️",
    layout="wide",
)

# ===============================
# CSS: FIX SIDEBAR, NAV BUTTONS & ACTIVE STATE
# ===============================
st.markdown("""
<style>
    /* 1. KEMBALIKAN HEADER STREAMLIT AGAR TOMBOL SIDEBAR MUNCUL */
    header {
        visibility: visible !important;
        background: transparent !important;
    }
    
    /* 2. PAKSA TOMBOL SIDEBAR (HAMBURGER) MUNCUL DI ATAS RUNNING TEXT */
    [data-testid="stSidebarCollapsedControl"] {
        z-index: 9999999 !important;
        color: #00ffea !important; /* Warna Ikon Hamburger */
        background-color: rgba(0,0,0,0.5); /* Latar kotak transparan biar jelas */
        border-radius: 5px;
        margin-top: 5px; /* Sesuaikan posisi vertikal */
        margin-left: 5px;
    }

    /* ====== BACKGROUND ====== */
    .stApp {
        background: radial-gradient(circle at top, #0a0f1f 0%, #050a18 50%, #02040a 100%);
        color: #d9e6ff;
    }

    /* ====== RUNNING TEXT (TOP FIXED) ====== */
    .running-text-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 45px; /* Sedikit diperlebar agar tombol menu muat enak */
        background: #000000;
        border-bottom: 2px solid #0056b3;
        z-index: 999999;
        display: flex;
        align-items: center;
        overflow: hidden;
    }
        
    .running-text {
        white-space: nowrap;
        animation: runText 35s linear infinite;
        font-family: 'Verdana', sans-serif;
        font-size: 14px;
        font-weight: bold;
        color: #00ffea;
        padding-left: 50px; /* Biar gak nabrak tombol sidebar */
    }
        
    @keyframes runText {
        0%   { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* Padding konten utama agar tidak ketutupan Running Text */
    .block-container {
        padding-top: 4rem !important; 
    }

    /* ============================================================ */
    /* ====== MODIFIKASI TOMBOL SIDEBAR (NAVIGASI) ================ */
    /* ============================================================ */
    
    /* 1. Sembunyikan lingkaran radio button default */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }

    /* 2. Ubah label teks menjadi TOMBOL KOTAK SERAGAM */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 12px 15px;
        margin-bottom: 8px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        
        /* Bikin lebar sama rata & teks di tengah/kiri */
        display: flex;
        align-items: center;
        width: 100% !important; /* SOLUSI UKURAN KOTAK TIDAK SAMA */
        justify-content: flex-start;
    }

    /* 3. Efek Hover */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background: rgba(0, 255, 234, 0.1);
        border-color: #00ffea;
        transform: translateX(5px);
    }

    /* 4. INDIKATOR AKTIF (SOLUSI MENANDAI FITUR YG DIBUKA) */
    /* Menggunakan selector :has(input:checked) untuk mendeteksi pilihan aktif */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(90deg, rgba(0,86,179,0.4), transparent) !important;
        border-left: 5px solid #00ffea !important; /* Garis Cyan di kiri */
        color: #00ffea !important; /* Teks jadi cyan */
        font-weight: bold;
        box-shadow: 0 0 15px rgba(0, 255, 234, 0.15);
    }

    /* 5. Background Sidebar */
    [data-testid="stSidebar"] {
        background: #050a15 !important;
        border-right: 1px solid #1f3a5f;
        margin-top: 45px; /* Turunkan sidebar di bawah running text */
    }

    /* ====== CARD STYLES ====== */
    .glass-card {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 15px;
    }
    
    .neon-title {
        font-size: 28px;
        font-weight: 700;
        color: #7cc7ff;
        margin-bottom: 20px;
        border-left: 5px solid #0056b3;
        padding-left: 15px;
    }
</style>

<!-- Running Text -->
<div class="running-text-container">
    <div class="running-text">
        ⚠️ INFO PENTING: MD5 tidak lagi disarankan untuk keamanan password tingkat tinggi karena risiko collision. Gunakan hanya untuk verifikasi integritas file & data non-krusial. ⚠️
    </div>
</div>
""", unsafe_allow_html=True)

# ===============================
# FUNGSI API (VIRUSTOTAL)
# ===============================
def check_vt_api(file_hash, api_key):
    """Mengambil data langsung dari Database Threat Intel"""
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": api_key}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            return "NOT_FOUND"
        elif response.status_code == 401:
            return "INVALID_KEY"
        else:
            return "ERROR"
    except:
        return "CONNECTION_ERROR"

# ===============================
# SIDEBAR NAVIGATION
# ===============================
with st.sidebar:
    st.markdown("<h2 style='color:#00ffea; text-align: center; margin-top: 10px;'>🛡️ MD5 Suite</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #8899aa; font-size: 12px;'>Futuristic Edition v8.0 (Final)</p>", unsafe_allow_html=True)
    st.write("") # Spacer
    
    # Menu Navigasi
    menu = st.radio("MAIN MENU", [
        "🏠 Single Check", 
        "📝 Text to MD5",
        "🚀 Batch Processor", 
        "🦠 Threat Intelligence",
        "🔓 Hash Cracker",
        "💪 Password Strength"
    ])
    st.markdown("---")

st.markdown(f"<div class='neon-title'>{menu}</div>", unsafe_allow_html=True)

# =========================================================
# MODE 1 — SINGLE CHECK
# =========================================================
if menu == "🏠 Single Check":
    tab1, tab2 = st.tabs(["📂 File vs File", "📝 File vs MD5"])
    
    with tab1:
        st.markdown("<div class='glass-card'>Bandingkan dua file untuk melihat apakah identik.</div>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: f1 = st.file_uploader("Upload File A", key="fileA")
        with c2: f2 = st.file_uploader("Upload File B", key="fileB")
            
        if f1 and f2:
            with st.spinner("Checking..."):
                h1, _ = bk.calculate_md5(f1)
                h2, _ = bk.calculate_md5(f2)
            
            if h1 == h2:
                st.success("✅ File IDENTIK (MD5 MATCH)")
            else:
                st.error("❌ File BERBEDA (MD5 MISMATCH)")
            st.code(f"MD5 A: {h1}\nMD5 B: {h2}")

    with tab2:
        st.markdown("<div class='glass-card'>Verifikasi integritas file dengan kode hash.</div>", unsafe_allow_html=True)
        file = st.file_uploader("Upload File", key="fileMd5")
        md5_text = st.text_input("Paste kode MD5 asli disini")
        
        if file and md5_text:
            file_hash, _ = bk.calculate_md5(file)
            if file_hash == md5_text.lower().strip():
                st.success("🎉 VERIFIED: File Asli & Aman")
            else:
                st.error("⚠️ WARNING: Hash tidak cocok!")
            st.code(f"Hash File: {file_hash}")

# =========================================================
# MODE 2 — TEXT TO MD5
# =========================================================
elif menu == "📝 Text to MD5":
    st.markdown("<div class='glass-card'>Ubah teks biasa menjadi hash MD5.</div>", unsafe_allow_html=True)
    
    text_input = st.text_area("Masukkan Teks/Kalimat", height=100)
    
    if st.button("Generate Hash"):
        if text_input:
            result = hashlib.md5(text_input.encode()).hexdigest()
            st.success("✅ Generated Successfully")
            st.code(result, language="text")
        else:
            st.warning("Masukkan teks dulu.")

# =========================================================
# MODE 3 — BATCH PROCESSOR
# =========================================================
elif menu == "🚀 Batch Processor":
    st.markdown("<div class='glass-card'>Generate hash untuk banyak file sekaligus.</div>", unsafe_allow_html=True)
    files = st.file_uploader("Pilih banyak file", accept_multiple_files=True)
    
    if files:
        if st.button("🚀 Proses Semua File"):
            with st.spinner("Sedang menghitung hash..."):
                df = bk.process_batch(files)
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download CSV", bk.convert_df_to_csv(df), "md5_report.csv")

# =========================================================
# MODE 4 — THREAT INTELLIGENCE
# =========================================================
elif menu == "🦠 Threat Intelligence":
    st.markdown("<div class='glass-card'>Cek reputasi file di database global threats (API Integrated).</div>", unsafe_allow_html=True)
    
    API_KEY_PERMANEN = "4c3d902295a016e36b6b59b03071db642fae870b15b7734513d235a661b742e9" 

    if API_KEY_PERMANEN:
        api_key = API_KEY_PERMANEN
    else:
        with st.expander("⚙️ Konfigurasi API"):
            api_key = st.text_input("Masukkan API Key", type="password", help="Dapatkan API Key gratis dari VirusTotal")
    
    file = st.file_uploader("Upload file mencurigakan")
    md5_text = st.text_input("Atau paste hash MD5 disini")
    
    md5_hash = None
    if file: 
        md5_hash, _ = bk.calculate_md5(file)
    elif md5_text: 
        md5_hash = md5_text

    if md5_hash:
        st.info(f"Target Hash: `{md5_hash}`")
        
        if st.button("🔍 Scan Database"):
            if not api_key:
                st.warning("⚠️ Masukkan API Key terlebih dahulu.")
                st.markdown(f"[Klik disini untuk cek manual di Web](https://www.virustotal.com/gui/file/{md5_hash})")
            else:
                with st.spinner("Menghubungi server intelijen..."):
                    data = check_vt_api(md5_hash, api_key)
                
                if data == "NOT_FOUND":
                    st.warning("🤔 File tidak ditemukan di database. Mungkin file baru atau belum pernah di-scan.")
                elif data == "INVALID_KEY":
                    st.error("❌ API Key Salah / Tidak Valid.")
                elif data == "ERROR" or data == "CONNECTION_ERROR":
                    st.error("❌ Gagal terhubung ke server.")
                else:
                    attr = data['data']['attributes']
                    stats = attr['last_analysis_stats']
                    malicious = stats['malicious']
                    
                    st.write("### 📊 Laporan Analisis")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Malicious (Berbahaya)", malicious, delta_color="inverse")
                    col2.metric("Suspicious (Curiga)", stats['suspicious'])
                    col3.metric("Harmless (Aman)", stats['harmless'])
                    
                    if malicious > 0:
                        st.error(f"🚨 BERBAHAYA! Terdeteksi oleh {malicious} vendor keamanan.")
                    else:
                        st.success("✅ AMAN. Tidak ada ancaman terdeteksi.")
                    
                    with st.expander("Lihat Detail Vendor Antivirus"):
                        st.json(stats)

                    st.markdown(f"""
                    <div style='background: rgba(0, 80, 255, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #0056b3; margin-top: 25px; font-size: 13px;'>
                        ℹ️ <b>Sumber Data:</b> Laporan ini diambil secara real-time dari database <b>VirusTotal™</b>.<br>
                        🔗 <a href="https://www.virustotal.com/gui/file/{md5_hash}" target="_blank" style="color: #00ffea; text-decoration: none; font-weight: bold;">
                            Klik disini untuk melihat laporan lengkap di Website Resmi ↗
                        </a>
                    </div>
                    """, unsafe_allow_html=True)

# =========================================================
# MODE 5 — HASH CRACKER
# =========================================================
elif menu == "🔓 Hash Cracker":
    st.markdown("""
    <div class='glass-card'>
        <b>🛠️ Dictionary Attack Tool</b><br>
        Mencoba memecahkan hash MD5 kembali menjadi teks menggunakan database password umum.
    </div>
    """, unsafe_allow_html=True)
    
    hash_input = st.text_input("Masukkan Target MD5 Hash")
    
    if st.button("💀 CRACK HASH", type="primary"):
        if not hash_input:
            st.warning("Mohon isi hash terlebih dahulu.")
        else:
            status = st.status("🚀 Memulai serangan dictionary...", expanded=True)
            status.write("📂 Memuat database...")
            time.sleep(0.5)
            
            try:
                result = bk.check_rockyou(hash_input, wordlist_path="rockyou.txt.tar.gz")
                
                status.update(label="Selesai!", state="complete", expanded=False)

                if result == "ERROR_NO_FILE":
                    st.error("❌ Database wordlist tidak ditemukan di server.")
                elif result and not result.startswith("ERROR"):
                    st.success("✅ PASSWORD DITEMUKAN!")
                    st.balloons()
                    st.markdown(f"## 🔓 {result}")
                elif result is None:
                    st.warning("🔒 GAGAL: Hash tidak ditemukan di database.")
                else:
                    st.error(result)
            except Exception as e:
                status.update(label="Error", state="error")
                st.error("Terjadi kesalahan sistem.")

# =========================================================
# MODE 6 — PASSWORD STRENGTH
# =========================================================
elif menu == "💪 Password Strength":
    st.markdown("<div class='glass-card'>Analisa kekuatan password teks biasa.</div>", unsafe_allow_html=True)
    
    pwd = st.text_input("Ketik Password", type="password")
    
    if pwd:
        skor = 0
        checks = {
            "Min 8 Karakter": len(pwd) >= 8,
            "Huruf Besar & Kecil": any(c.islower() for c in pwd) and any(c.isupper() for c in pwd),
            "Angka": any(c.isdigit() for c in pwd),
            "Simbol Unik": any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for c in pwd),
            "Panjang 12+": len(pwd) >= 12,
        }
        
        for check in checks.values():
            if check: skor += 1
            
        labels = ["Sangat Lemah", "Lemah", "Cukup", "Kuat", "Sangat Kuat"]
        final_label = labels[max(0, skor - 1)]
        
        st.markdown(f"### Skor: {skor}/5 — {final_label}")
        st.progress(skor / 5)
        
        st.write("---")
        for rule, passed in checks.items():
            st.write(f"{'✅' if passed else '❌'} {rule}")