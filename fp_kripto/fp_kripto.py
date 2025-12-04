# ============================================
# app.py — MD5 Suite Futuristic UI Edition
# ============================================

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
# FUTURISTIC CSS (Neon + Glass)
# ===============================
st.markdown("""
<style>

    /* Background gradient */
    .stApp {
        background: radial-gradient(circle at top,
            #0a0f1f 0%, 
            #0a0f1f 40%,
            #030611 100%);
        color: #d9e6ff;
    }

    /* Glassmorphism card */
    .glass-card {
        background: rgba(255, 255, 255, 0.06);
        padding: 22px;
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.12);
        backdrop-filter: blur(12px);
        box-shadow: 0 0 16px rgba(0, 150, 255, 0.15);
        margin-bottom: 15px;
    }

    /* Neon text */
    .neon-title {
        font-size: 34px;
        font-weight: 700;
        color: #7cc7ff;
        text-shadow: 0 0 10px rgba(0,150,255,0.8);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.08);
        border-radius: 6px;
        padding: 8px 12px;
        color: #b8d4ff;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background: #148AFF !important;
        color: white !important;
        box-shadow: 0 0 10px #148AFF;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: rgba(0, 30, 60, 0.6);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255,255,255,0.1);
    }

    /* Table */
    [data-testid="stDataFrame"] {
        border-radius: 10px !important;
    }

</style>
""", unsafe_allow_html=True)

# ===============================
# SIDEBAR
# ===============================
with st.sidebar:
    st.markdown("<h1 style='color:#93c7ff;'>🛡️ MD5 Suite</h1>", unsafe_allow_html=True)
    st.caption("Futuristic Edition v3.0")

    menu = st.radio(
        "Navigation",
        ["🏠 Single Check", "🚀 Batch Processor", "🦠 Malware Intel", "🔓 Hash Cracker"]
    )

    st.markdown("---")
    st.caption("Created with ❤️ Streamlit")


# ===============================
# DYNAMIC HEADER
# ===============================
st.markdown(f"<div class='neon-title'>{menu}</div>", unsafe_allow_html=True)
st.write("")

# =========================================================
# MODE 1 — SINGLE CHECK
# =========================================================
if menu == "🏠 Single Check":

    tab1, tab2 = st.tabs(["📂 File vs File", "📝 File vs MD5"])

    # --- FILE VS FILE ---
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
                st.balloons()
            else:
                st.error("❌ File BERBEDA (MD5 MISMATCH)")

            st.code(f"MD5 A: {h1}")
            st.code(f"MD5 B: {h2}")

    # --- FILE vs TEXT ---
    with tab2:
        file = st.file_uploader("Upload File", key="fileMd5")
        md5_text = st.text_input("Masukkan MD5")

        if file and md5_text:
            file_hash, _ = bk.calculate_md5(file)
            st.write("Hash File:", file_hash)

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

            st.success("Selesai!")
            st.dataframe(df, use_container_width=True)

            st.download_button("⬇️ Download CSV", bk.convert_df_to_csv(df), "report.csv")


# =========================================================
# MODE 3 — MALWARE INTEL
# =========================================================
elif menu == "🦠 Malware Intel":

    file = st.file_uploader("Upload file mencurigakan")
    md5_text = st.text_input("Atau masukkan hash")

    if file:
        md5_hash, _ = bk.calculate_md5(file)
    elif md5_text:
        md5_hash = md5_text
    else:
        md5_hash = None

    if md5_hash:
        st.info(f"MD5: `{md5_hash}`")
        vt_link = bk.get_virustotal_link(md5_hash)
        st.markdown(f"[🔍 Cek VirusTotal]({vt_link})")


# =========================================================
# MODE 4 — HASH CRACKER
# =========================================================
elif menu == "🔓 Hash Cracker":

    hash_input = st.text_input("Masukkan MD5 hash")
    if st.button("🔓 Crack"):

        result = bk.check_weak_password(hash_input)

        if result:
            st.error("⚠️ CRACKED! Password ditemukan:")
            st.code(result)
        else:
            st.success("Hash tidak ada di database password lemah.")
