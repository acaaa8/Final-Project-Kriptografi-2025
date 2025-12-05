import streamlit as st
import hashlib
import requests
import backend as bk  # Pastikan backend.py ada

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MD5 Toolkit",
    page_icon="⚡",
    layout="wide",
)

# ===============================
# CSS: UI MODERN & SIDEBAR FIX
# ===============================
st.markdown("""
<style>
    /* 1. FIX HEADER & SIDEBAR BUTTON */
    header {
        visibility: visible !important;
        background: transparent !important;
    }
    [data-testid="stSidebarCollapsedControl"] {
        z-index: 9999999 !important;
        color: #00ffea !important;
        background-color: rgba(0,0,0,0.5);
        border-radius: 5px;
        margin-top: 5px;
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
        height: 45px;
        background: #000000;
        border-bottom: 2px solid #0056b3;
        z-index: 999999;
        display: flex;
        align-items: center;
        overflow: hidden;
    }
        
    .running-text {
        white-space: nowrap;
        animation: runText 40s linear infinite;
        font-family: 'Verdana', sans-serif;
        font-size: 14px;
        font-weight: bold;
        color: #00ffea;
        padding-left: 50px;
    }
        
    @keyframes runText {
        0%   { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* Padding konten utama */
    .block-container {
        padding-top: 4rem !important; 
    }

    /* ====== TOMBOL NAVIGASI SIDEBAR ====== */
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label {
        background: rgba(255, 255, 255, 0.05);
        padding: 12px 15px;
        margin-bottom: 8px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
        width: 100% !important;
        justify-content: flex-start;
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        background: rgba(0, 255, 234, 0.1);
        border-color: #00ffea;
        transform: translateX(5px);
    }
    [data-testid="stSidebar"] [data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(90deg, rgba(0,86,179,0.4), transparent) !important;
        border-left: 5px solid #00ffea !important;
        color: #00ffea !important;
        font-weight: bold;
        box-shadow: 0 0 15px rgba(0, 255, 234, 0.15);
    }
    [data-testid="stSidebar"] {
        background: #050a15 !important;
        border-right: 1px solid #1f3a5f;
        margin-top: 45px;
    }

    /* ====== CARD STYLES ====== */
    .glass-card {
        background: rgba(255,255,255,0.05);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 15px;
    }
    .info-text {
        color: #aab;
        font-size: 14px;
        margin-bottom: 10px;
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
        ℹ️ INFO: Aplikasi ini menggunakan algoritma MD5 (Digital Fingerprint). Gunakan untuk memverifikasi integritas file atau pemindaian keamanan cepat.
    </div>
</div>
""", unsafe_allow_html=True)

# ===============================
# FUNGSI API (VIRUSTOTAL)
# ===============================
def check_vt_api(file_hash, api_key):
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
    st.markdown("<h2 style='color:#00ffea; text-align: center; margin-top: 10px;'>⚡MD5 Toolkit</h2>", unsafe_allow_html=True)
    st.write("") # Spacer
    
    # --- Menu Utama ---
    menu = st.radio("MAIN MENU", [
        "📂 File Integrity Check",
        "🔏 MD5 Generator",         # <-- NAMA DIUBAH BIAR LEBIH KEREN
        "📦 Multiple File Hashing",
        "🛡️ File Safety Scan"
    ])
    st.markdown("---")

st.markdown(f"<div class='neon-title'>{menu}</div>", unsafe_allow_html=True)

# =========================================================
# MODE 1 — FILE INTEGRITY CHECK
# =========================================================
if menu == "📂 File Integrity Check":
    st.markdown("""
    <div class='glass-card'>
        <b>ℹ️ Tentang Fitur Ini:</b><br>
        <span class='info-text'>
        Memastikan file yang Anda punya <b>asli dan tidak rusak</b>. Gunakan ini untuk membandingkan file dengan file lain, atau dengan kode hash dari website download.
        </span>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Compare Two Files", "Verify with MD5"])
    
    with tab1:
        st.write("### Bandingkan 2 File")
        st.caption("Upload dua file untuk melihat apakah isinya sama.")
        c1, c2 = st.columns(2)
        with c1: f1 = st.file_uploader("Upload File Pertama", key="fileA")
        with c2: f2 = st.file_uploader("Upload File Kedua", key="fileB")
            
        if f1 and f2:
            with st.spinner("Sedang membandingkan..."):
                h1, _ = bk.calculate_md5(f1)
                h2, _ = bk.calculate_md5(f2)
            
            if h1 == h2:
                st.success("✅ HASIL: SAMA (Isi file sama persis)")
            else:
                st.error("❌ HASIL: Berbeda (Isi file tidak sama)")
            st.code(f"Kode File 1: {h1}\nKode File 2: {h2}")

    with tab2:
        st.write("### Verifikasi dengan Kode")
        st.caption("Cocokkan file dengan kode MD5 yang Anda punya.")
        file = st.file_uploader("Upload File", key="fileMd5")
        md5_text = st.text_input("Tempel kode MD5 asli disini")
        
        if file and md5_text:
            file_hash, _ = bk.calculate_md5(file)
            if file_hash == md5_text.lower().strip():
                st.success("🎉 VERIFIED: File Asli & Aman")
            else:
                st.error("⚠️ WARNING: Kode tidak cocok! File mungkin rusak atau palsu.")
            st.code(f"Kode File Anda: {file_hash}")

# =========================================================
# MODE 2 — MD5 GENERATOR (DITINGKATKAN)
# =========================================================
elif menu == "🔏 MD5 Generator":
    st.markdown("""
    <div class='glass-card'>
        <b>ℹ️ Tentang Fitur Ini:</b><br>
        <span class='info-text'>
        Membuat kode MD5 (Hashing) dari <b>Teks</b> maupun <b>File</b>. Fitur ini berguna jika Anda ingin mengetahui kode hash tanpa melakukan pembandingan dengan file lain.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # Menggunakan Tabs agar support Text dan File
    tab_txt, tab_file = st.tabs(["🔤 From Text", "📂 From File"])
    
    # --- GENERATE DARI TEXT ---
    with tab_txt:
        st.write("### Teks ke MD5")
        text_input = st.text_area("Masukkan Teks/Kalimat", height=100, placeholder="Ketik sesuatu...")
        if st.button("Generate Hash Teks"):
            if text_input:
                result = hashlib.md5(text_input.encode()).hexdigest()
                st.success("✅ Berhasil")
                st.code(result, language="text")
            else:
                st.warning("Masukkan teks dulu.")

    # --- GENERATE DARI FILE ---
    with tab_file:
        st.write("### File ke MD5")
        uploaded_file = st.file_uploader("Upload satu file", key="single_gen")
        if uploaded_file:
            with st.spinner("Menghitung hash..."):
                # Hitung hash
                file_hash, _ = bk.calculate_md5(uploaded_file)
                st.success("✅ Berhasil")
                st.write("Kode MD5 File:")
                st.code(file_hash, language="text")
                st.caption(f"Nama File: {uploaded_file.name}")

# =========================================================
# MODE 3 — Multiple File Hashing
# =========================================================
elif menu == "📦 Multiple File Hashing":
    st.markdown("""
    <div class='glass-card'>
        <b>ℹ️ Tentang Fitur Ini:</b><br>
        <span class='info-text'>
        Memproses <b>banyak file sekaligus</b>. Jika Anda perlu mendata kode unik (checksum) dari ratusan file secara otomatis, gunakan fitur ini.
        </span>
    </div>
    """, unsafe_allow_html=True)

    files = st.file_uploader("Pilih banyak file (Drag & Drop)", accept_multiple_files=True)
    
    if files:
        if st.button("🚀 Mulai Proses"):
            with st.spinner("Sedang menghitung..."):
                df = bk.process_batch(files)
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download Laporan (CSV)", bk.convert_df_to_csv(df), "laporan_file.csv")

# =========================================================
# MODE 4 — FILE SAFETY SCAN
# =========================================================
elif menu == "🛡️ File Safety Scan":
    st.markdown("""
    <div class='glass-card'>
        <b>ℹ️ Tentang Fitur Ini:</b><br>
        <span class='info-text'>
        Mengecek apakah sebuah file <b>berbahaya (virus/malware)</b>. 
        <br>🔒 <b>Privasi Dijamin:</b> File Anda <b>TIDAK</b> diupload. Kami hanya mengirimkan Hash MD5 file ke database 
        <a href='https://www.virustotal.com/' target='_blank' style='color:#00ffea; text-decoration:none; font-weight:bold;'>VirusTotal™</a>.
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    # API KEY (Hardcoded sesuai input user sebelumnya)
    API_KEY_PERMANEN = "4c3d902295a016e36b6b59b03071db642fae870b15b7734513d235a661b742e9" 

    if API_KEY_PERMANEN:
        api_key = API_KEY_PERMANEN
    else:
        with st.expander("⚙️ Pengaturan Akses"):
            api_key = st.text_input("Masukkan Kunci Akses (API Key)", type="password")
    
    col_a, col_b = st.columns(2)
    with col_a:
        file = st.file_uploader("Opsi 1: Upload File (Otomatis Hitung Hash)")
    with col_b:
        md5_text = st.text_input("Opsi 2: Masukkan Kode Hash Manual")
    
    md5_hash = None
    if file: 
        md5_hash, _ = bk.calculate_md5(file)
    elif md5_text: 
        md5_hash = md5_text

    if md5_hash:
        st.info(f"Kode Unik File: `{md5_hash}`")
        
        if st.button("🔍 Cek Keamanan"):
            if not api_key:
                st.warning("⚠️ Kunci akses belum diisi.")
            else:
                with st.spinner("Sedang menghubungi database keamanan..."):
                    data = check_vt_api(md5_hash, api_key)
                
                if data == "NOT_FOUND":
                    st.warning("🤔 File tidak dikenal (Unknown). File mungkin bersih atau belum pernah dideteksi sebelumnya.")
                elif data == "INVALID_KEY":
                    st.error("❌ Kunci akses salah.")
                elif data == "ERROR" or data == "CONNECTION_ERROR":
                    st.error("❌ Gagal terhubung ke server.")
                else:
                    attr = data['data']['attributes']
                    stats = attr['last_analysis_stats']
                    malicious = stats['malicious']
                    
                    st.write("### 📊 Hasil Analisis")
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Terdeteksi Bahaya", malicious, delta_color="inverse")
                    col2.metric("Mencurigakan", stats['suspicious'])
                    col3.metric("Aman (Clean)", stats['harmless'])
                    
                    if malicious > 0:
                        st.error(f"🚨 BERBAHAYA! File ini ditandai bahaya oleh {malicious} antivirus.")
                    else:
                        st.success("✅ AMAN. Tidak ada ancaman yang ditemukan pada file ini.")
                    
                    with st.expander("Lihat Detail Deteksi"):
                        st.json(stats)

                    st.markdown(f"""
                    <div style='background: rgba(0, 80, 255, 0.1); padding: 15px; border-radius: 10px; border-left: 4px solid #0056b3; margin-top: 25px; font-size: 13px;'>
                        ℹ️ <b>Sumber Data:</b> Laporan diambil dari database <b>VirusTotal™</b>.<br>
                        🔗 <a href="https://www.virustotal.com/gui/file/{md5_hash}" target="_blank" style="color: #00ffea; text-decoration: none; font-weight: bold;">
                            Lihat laporan lengkap di Website Resmi ↗
                        </a>
                    </div>
                    """, unsafe_allow_html=True)