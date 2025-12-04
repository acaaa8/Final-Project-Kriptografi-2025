import streamlit as st
import time
import pandas as pd
import backend as bk

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="MD5 Ultimate Suite",
    page_icon="🛡️",
    layout="wide",
)

# ===============================
# FUTURISTIC CSS
# ===============================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top, #0a0f1f 0%, #0a0f1f 40%, #030611 100%);
        color: #d9e6ff;
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        padding: 22px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.12);
        backdrop-filter: blur(12px);
        margin-bottom: 15px;
    }
    .neon-title {
        font-size: 34px; font-weight: 700; color: #7cc7ff;
        text-shadow: 0 0 10px rgba(0,150,255,0.8);
    }
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.08); color: #b8d4ff;
    }
    .stTabs [aria-selected="true"] {
        background: #148AFF !important; color: white !important;
    }
    [data-testid="stSidebar"] {
        background: rgba(0, 30, 60, 0.6); backdrop-filter: blur(10px);
    }
</style>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.markdown("<h1 style='color:#93c7ff;'>🛡️ MD5 Suite</h1>", unsafe_allow_html=True)
    st.caption("Futuristic Edition v3.0 (RockYou Fixed)")
    menu = st.radio("Navigation", ["🏠 Single Check", "🚀 Batch Processor", "🦠 Malware Intel", "🔓 Hash Cracker"])
    st.markdown("---")

st.markdown(f"<div class='neon-title'>{menu}</div>", unsafe_allow_html=True)
st.write("")

# =========================================================
# MODE 1 — SINGLE CHECK
# =========================================================
if menu == "🏠 Single Check":
    tab1, tab2 = st.tabs(["📂 File vs File", "📝 File vs MD5"])
    
    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("<div class='glass-card'>Upload File Asli</div>", unsafe_allow_html=True)
            f1 = st.file_uploader("File A", key="fileA")
        with c2:
            st.markdown("<div class='glass-card'>Upload File Target</div>", unsafe_allow_html=True)
            f2 = st.file_uploader("File B", key="fileB")
        if f1 and f2:
            with st.spinner("🔍 Processing..."):
                h1, s1 = bk.calculate_md5(f1)
                h2, s2 = bk.calculate_md5(f2)
            if h1 == h2:
                st.success("✅ File IDENTIK (MD5 MATCH)")
            else:
                st.error("❌ File BERBEDA (MD5 MISMATCH)")
            st.code(f"MD5 A: {h1}")
            st.code(f"MD5 B: {h2}")

    with tab2:
        file = st.file_uploader("Upload File", key="fileMd5")
        md5_text = st.text_input("Masukkan MD5")
        if file and md5_text:
            file_hash, _ = bk.calculate_md5(file)
            if file_hash == md5_text.lower().strip():
                st.success("🎉 MD5 MATCH")
            else:
                st.error("⚠️ Tidak cocok")

# =========================================================
# MODE 2 — BATCH PROCESSOR
# =========================================================
elif menu == "🚀 Batch Processor":
    st.markdown("<div class='glass-card'>Upload banyak file sekaligus untuk audit massal</div>", unsafe_allow_html=True)
    files = st.file_uploader("Upload multiple files", accept_multiple_files=True)
    if files:
        if st.button("🚀 Mulai Proses"):
            with st.spinner("Processing..."):
                df = bk.process_batch(files)
            st.dataframe(df, use_container_width=True)
            st.download_button("⬇️ Download CSV", bk.convert_df_to_csv(df), "report.csv")

# =========================================================
# MODE 3 — MALWARE INTEL
# =========================================================
elif menu == "🦠 Malware Intel":
    file = st.file_uploader("Upload file mencurigakan")
    md5_text = st.text_input("Atau masukkan hash")
    if file: md5_hash, _ = bk.calculate_md5(file)
    elif md5_text: md5_hash = md5_text
    else: md5_hash = None
    if md5_hash:
        st.info(f"MD5: `{md5_hash}`")
        vt_link = bk.get_virustotal_link(md5_hash)
        st.markdown(f"[🔍 Cek VirusTotal]({vt_link})")

# =========================================================
# MODE 4 — HASH CRACKER (FIXED)
# =========================================================
elif menu == "🔓 Hash Cracker":
    st.markdown("<div class='glass-card'>Brute-Force menggunakan <b>rockyou.txt.tar.gz</b></div>", unsafe_allow_html=True)
    
    hash_input = st.text_input("Target MD5 Hash", placeholder="Paste hash disini...")
    
    if st.button("💀 CRACK NOW", type="primary"):
        if not hash_input:
            st.warning("Isi hash dulu!")
        else:
            status = st.status("🚀 Sedang mencari di database hacker...", expanded=True)
            status.write("📂 Membuka arsip rockyou.txt.tar.gz...")
            time.sleep(0.5)
            
            # --- PANGGIL FUNGSI BARU ---
            # Pastikan nama file sesuai dengan yang ada di foldermu
            result = bk.check_rockyou(hash_input, wordlist_path="rockyou.txt.tar.gz")
            # ---------------------------
            
            status.update(label="Selesai!", state="complete", expanded=False)

            if result == "ERROR_NO_FILE":
                st.error("❌ File 'rockyou.txt.tar.gz' tidak ditemukan di folder script!")
            elif result and not result.startswith("ERROR"):
                st.success("✅ PASSWORD FOUND!")
                st.markdown(f"## 🎉 {result}")
                st.balloons()
            elif result is None:
                st.warning("🔒 PASSWORD NOT FOUND (Aman/Tidak ada di list)")
            else:
                st.error(result)