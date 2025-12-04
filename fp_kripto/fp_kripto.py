import streamlit as st
import backend as bk  # Import file backend yang tadi dibuat
import time
import pandas as pd

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="MD5 Ultimate Suite", page_icon="☢️", layout="wide")

# --- CSS MODERN (DIPERBARUI) ---
st.markdown("""
<style>
    :root { --primary: #A8DADC; --bg: #1D3557; --card: #243E63; }
    .stApp { background-color: var(--bg); color: #F1FAEE; }
    
    /* Card Style */
    .feature-card {
        background-color: var(--card);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(168,218,220,0.1);
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] { color: #E63946 !important; }
    
    /* Table styling */
    [data-testid="stDataFrame"] { border: 1px solid #457B9D; border-radius: 10px; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #162945; }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR NAVIGATION =====
with st.sidebar:
    st.title("☢️ MD5 Suite")
    st.markdown("---")
    menu = st.radio("Pilih Mode:", 
        ["🏠 Single Check", "🚀 Batch Processor", "🦠 Malware Intel", "🔓 Hash Cracker (Demo)"])
    
    st.markdown("---")
    st.info("💡 **Tips:** Gunakan Batch Processor untuk mengaudit satu folder sekaligus.")

# ===== HEADER =====
st.title(f"{menu}")
st.write("Professional File Integrity & Security Tool")
st.divider()

# =========================================================
# MODE 1: SINGLE CHECK (File vs File)
# =========================================================
if menu == "🏠 Single Check":
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📄 File Referensi")
        f1 = st.file_uploader("Upload File Asli", key="f1")
    with col2:
        st.markdown("### 📄 File Target")
        f2 = st.file_uploader("Upload File Banding", key="f2")

    if f1 and f2:
        st.markdown("---")
        with st.spinner("Analyzing bitstream..."):
            h1, s1 = bk.calculate_md5(f1)
            h2, s2 = bk.calculate_md5(f2)
            time.sleep(0.3) # Efek visual

        # Metrics Speed
        m1, m2, m3 = st.columns(3)
        m1.metric("File 1 Speed", f"{s1:.1f} MB/s")
        m2.metric("File 2 Speed", f"{s2:.1f} MB/s")
        m3.metric("Diff Status", "MATCH" if h1==h2 else "DIFFERENT")

        # Visual Result
        if h1 == h2:
            st.success(f"✅ **INTEGRITY CONFIRMED**: Hash {h1}")
            st.balloons()
        else:
            st.error("❌ **INTEGRITY FAILED**: File tidak sama.")
            c_res1, c_res2 = st.columns(2)
            c_res1.code(h1, language="text")
            c_res2.code(h2, language="text")

# =========================================================
# MODE 2: BATCH PROCESSOR (Fitur Baru Terbesar)
# =========================================================
elif menu == "🚀 Batch Processor":
    st.markdown("<div class='feature-card'>Fitur ini memungkinkan Anda memeriksa puluhan file sekaligus dan mengekspor laporannya.</div>", unsafe_allow_html=True)
    
    files = st.file_uploader("Drag & Drop Banyak File Di Sini", accept_multiple_files=True)
    
    if files:
        if st.button(f"🚀 Proses {len(files)} File"):
            progress_bar = st.progress(0)
            
            # Proses Backend
            df = bk.process_batch(files)
            progress_bar.progress(100)
            
            # Tampilkan Tabel
            st.subheader("📊 Hasil Audit Hash")
            st.dataframe(df, use_container_width=True)
            
            # Download CSV
            csv = bk.convert_df_to_csv(df)
            st.download_button(
                label="⬇️ Download Laporan CSV",
                data=csv,
                file_name="md5_batch_report.csv",
                mime="text/csv",
                type="primary"
            )

# =========================================================
# MODE 3: MALWARE INTEL (VirusTotal)
# =========================================================
elif menu == "🦠 Malware Intel":
    st.markdown("<div class='feature-card'>Cek apakah hash file Anda dikenali sebagai virus oleh database global.</div>", unsafe_allow_html=True)
    
    col_virus_1, col_virus_2 = st.columns([1, 2])
    
    with col_virus_1:
        f_virus = st.file_uploader("Upload File Mencurigakan")
    
    with col_virus_2:
        st.info("Atau paste hash MD5 jika sudah punya:")
        hash_input = st.text_input("MD5 Hash", placeholder="Paste hash disini...")

    final_hash = None
    if f_virus:
        final_hash, _ = bk.calculate_md5(f_virus)
        st.success(f"File Hash Detected: `{final_hash}`")
    elif hash_input:
        final_hash = hash_input.strip()

    if final_hash:
        vt_link = bk.get_virustotal_link(final_hash)
        st.markdown(f"""
        ### 🔍 Analisis Keamanan
        Klik tombol di bawah untuk membuka **VirusTotal Search**. Jika file ini adalah virus yang sudah dikenal, VirusTotal akan memberitahu Anda.
        """)
        st.link_button("🛡️ Cek di VirusTotal Database", vt_link)

# =========================================================
# MODE 4: HASH CRACKER (Demo Password Lemah)
# =========================================================
elif menu == "🔓 Hash Cracker (Demo)":
    st.markdown("<div class='feature-card'>Mendemonstrasikan bahaya menggunakan password lemah. Sistem akan mencocokkan hash dengan database password umum.</div>", unsafe_allow_html=True)
    
    crack_input = st.text_input("Masukkan MD5 Hash (Contoh: e10adc3949ba59abbe56e057f20f883e)", help="Coba hash dari '123456'")
    
    if st.button("🔓 Coba Pecahkan"):
        if not crack_input:
            st.warning("Masukkan hash dulu.")
        else:
            with st.spinner("Melakukan Dictionary Attack..."):
                time.sleep(1) # Suspense
                result = bk.check_weak_password(crack_input.strip().lower())
            
            if result:
                st.error("⚠️ **CRACKED! HASH BERHASIL DIPECAHKAN**")
                st.metric("Password Asli", result)
                st.write("Hash ini berasal dari password yang sangat lemah.")
            else:
                st.success("🔒 **SAFE (Not Found)**")
                st.write("Hash tidak ditemukan di database password lemah (Top 20 common).")