import streamlit as st
import hashlib

# --- FUNGSI BACKEND ---
def hitung_md5(uploaded_file):
    md5 = hashlib.md5()
    for chunk in iter(lambda: uploaded_file.read(4096), b""):
        md5.update(chunk)
    uploaded_file.seek(0)
    return md5.hexdigest()


# --- TAMPILAN WEBSITE (FRONTEND) ---
st.set_page_config(page_title="MD5 File Checksum Verifier", page_icon="🔒")

# 🎨 TEMA WARNA BERDASARKAN PALET YANG KAMU KASIH
st.markdown("""
<style>
.stApp {
    background-color: #1D3557;          /* Prussian Blue */
    color: #F1FAEE;                     /* Honeydew */
}

/* JUDUL */
h1, h2, h3 {
    color: #A8DADC !important;          /* Powder Blue */
    font-weight: 700;
}

/* DIVIDER */
hr { border-top: 2px solid #A8DADC !important; }

/* ========================================== */
/*  FILE UPLOADER BOX  (drag & drop + batas)  */
/* ========================================== */
[data-testid="stFileUploader"] > div {
    background-color: #457B9D !important;      /* Celadon Blue */
    border-radius: 12px;
    border: 2px dashed #A8DADC !important;      /* Powder Blue border */
}

/* Text di area drag & drop */
[data-testid="stFileUploader"] * {
    color: #F1FAEE !important;
}

/* Tombol Browse File */
[data-testid="stFileUploader"] button {
    background-color: #A8DADC !important;      /* Powder Blue */
    color: #1D3557 !important;                 /* Dark biar kebaca */
    font-weight: 700;
    padding: 6px 16px;
    border-radius: 10px;
}

/* Hover tombol */
[data-testid="stFileUploader"] button:hover {
    background-color: #E63946 !important;      /* Red */
    color: white !important;
}

/* SUCCESS BOX */
.stSuccess {
    background-color: rgba(168,218,220,0.12) !important;
    border-left: 6px solid #A8DADC !important;
    color: #F1FAEE !important;
}

/* ERROR BOX */
.stError {
    background-color: rgba(230,57,70,0.12) !important;
    border-left: 6px solid #E63946 !important;
    color: #F1FAEE !important;
}

/* WARNING BOX */
.stWarning {
    background-color: rgba(255,255,255,0.1) !important;
    border-left: 6px solid #457B9D !important;
    color: #F1FAEE !important;
}

/* INFO BOX */
.stInfo {
    background-color: rgba(255,255,255,0.05) !important;
    border-left: 6px solid #457B9D !important;
    color: #F1FAEE !important;
}

/* CODE BLOCK */
code, pre {
    background-color: rgba(168,218,220,0.16) !important;
    color: #F1FAEE !important;
    border-radius: 6px;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# ===== UI UTAMA =====
st.title("🔒 MD5 File Checksum Verifier")
st.write("Upload dua file untuk membandingkan integritas dan kesamaan keduanya melalui nilai hash MD5.")

# Layout kolom (asli — tidak diubah)
col1, col2 = st.columns(2)

with col1:
    st.subheader("File 1")
    file_upload_1 = st.file_uploader("Pilih File Pertama", type=None, key="file1")
    hash_1 = None

with col2:
    st.subheader("File 2")
    file_upload_2 = st.file_uploader("Pilih File Kedua", type=None, key="file2")
    hash_2 = None

st.divider()
st.subheader("Hasil Perbandingan Otomatis")

# ===== LOGIKA PERHITUNGAN =====
if file_upload_1 is not None and file_upload_2 is not None:

    with st.spinner("Menghitung MD5 File 1..."):
        hash_1 = hitung_md5(file_upload_1)

    with st.spinner("Menghitung MD5 File 2..."):
        hash_2 = hitung_md5(file_upload_2)

    with col1:
        st.info(f"File 1: **{file_upload_1.name}**")
        st.code(hash_1, language='text')

    with col2:
        st.info(f"File 2: **{file_upload_2.name}**")
        st.code(hash_2, language='text')

    st.markdown("---")

    if hash_1 == hash_2:
        st.success("🎉 **VALID! KEDUA FILE COCOK!**")
        st.write("Hash MD5 dari File 1 dan File 2 identik.")
        st.balloons()
    else:
        st.error("❌ **TIDAK COCOK!**")
        st.write("Hash MD5 dari kedua file berbeda. Salah satu file mungkin korup, berbeda, atau telah dimodifikasi.")
        st.write(f"MD5 File 1: `{hash_1}`")
        st.write(f"MD5 File 2: `{hash_2}`")

elif file_upload_1 is not None or file_upload_2 is not None:
    st.warning("Silakan upload kedua file untuk memulai perbandingan.")

else:
    st.caption("Silakan upload kedua file di atas untuk membandingkan hash MD5 secara instan.")
