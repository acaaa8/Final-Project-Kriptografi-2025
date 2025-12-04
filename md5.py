import streamlit as st
import hashlib
import time

# --- FUNGSI BACKEND ---
def hitung_md5(uploaded_file):
    """Menghitung hash MD5 dari file object."""
    md5 = hashlib.md5()
    uploaded_file.seek(0)
    for chunk in iter(lambda: uploaded_file.read(4096), b""):
        md5.update(chunk)
    uploaded_file.seek(0)
    return md5.hexdigest()

def hash_string(text):
    """Menghitung MD5 dari string teks."""
    return hashlib.md5(text.encode()).hexdigest()

def get_identicon(md5_hash):
    """Link API untuk generate avatar unik berdasarkan hash."""
    return f"https://api.dicebear.com/9.x/identicon/svg?seed={md5_hash}&backgroundColor=transparent"

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="MD5 Pro Verifier", page_icon="🛡️", layout="wide")

# --- UI / CSS UPGRADE (MODERN LOOK) ---
st.markdown("""
<style>
    /* --- PALET WARNA --- */
    :root {
        --bg-dark: #1D3557;
        --card-bg: #2b466b;
        --primary: #A8DADC;
        --accent: #E63946;
        --text: #F1FAEE;
    }

    /* --- GLOBAL --- */
    .stApp {
        background-color: var(--bg-dark);
        color: var(--text);
    }
    
    /* --- CARD DESIGN CONTAINER --- */
    .css-card {
        background-color: var(--card-bg);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        border: 1px solid rgba(168, 218, 220, 0.1);
    }

    /* --- HEADERS --- */
    h1, h2, h3 {
        color: var(--primary) !important;
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* --- FILE UPLOADER CUSTOM --- */
    [data-testid="stFileUploader"] {
        padding: 10px;
    }
    [data-testid="stFileUploader"] section {
        background-color: rgba(168, 218, 220, 0.05);
        border: 2px dashed var(--primary);
        border-radius: 10px;
    }

    /* --- CODE BLOCKS --- */
    code {
        color: #F4A261 !important;
        background: rgba(0,0,0,0.3) !important;
        font-size: 1.1em;
        font-weight: bold;
        padding: 5px 10px;
        border-radius: 5px;
    }

    /* --- TABS --- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(0,0,0,0.2);
        padding: 10px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 8px;
        color: var(--text);
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--accent);
        color: white;
    }

    /* --- BUTTONS --- */
    .stButton button {
        background-color: var(--primary);
        color: #1D3557;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        transition: all 0.3s;
    }
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(168, 218, 220, 0.4);
    }
    
    /* --- RESULT BOX ANIMATION --- */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .result-box {
        animation: fadeIn 0.5s ease-out;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# ===== SIDEBAR INFO =====
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/MD5_algorithm_simulated_icon.svg/1200px-MD5_algorithm_simulated_icon.svg.png", width=100)
    st.title("Tentang MD5")
    st.info("""
    **MD5 (Message-Digest Algorithm 5)** adalah fungsi hash kriptografik yang menghasilkan nilai 128-bit (32 karakter hex).
    
    **Kegunaan:**
    - Verifikasi integritas file (download corrupt?)
    - Validasi identitas data
    
    **Catatan:**
    MD5 tidak lagi disarankan untuk keamanan password tingkat tinggi (karena *collision*), tetapi sangat cepat dan efektif untuk cek integritas file.
    """)
    st.markdown("---")
    st.caption("Developed with Streamlit")

# ===== HEADER UTAMA =====
st.title("🛡️ MD5 Pro Verifier")
st.markdown("### Toolkit Lengkap Validasi Integritas Data")

# ===== TABS MENU =====
tab1, tab2, tab3 = st.tabs(["📂 File vs File", "📝 File vs Kode", "🔤 Teks ke MD5"])

# =========================================================
# TAB 1: FILE VS FILE (Dengan Visual Hash)
# =========================================================
with tab1:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.write("Bandingkan dua file untuk melihat apakah mereka 100% identik.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📁 File A")
        file_a = st.file_uploader("Upload File Pertama", key="fa")
    
    with col2:
        st.subheader("📁 File B")
        file_b = st.file_uploader("Upload File Kedua", key="fb")
    
    if file_a and file_b:
        st.markdown("---")
        with st.spinner("🚀 Memproses Hashing & Visualisasi..."):
            hash_a = hitung_md5(file_a)
            hash_b = hitung_md5(file_b)
            # Simulasi delay agar terlihat smooth (opsional)
            time.sleep(0.5)

        # Hasil Side-by-Side dengan Visual Hash
        res_c1, res_c2 = st.columns(2)
        
        with res_c1:
            st.markdown(f"**{file_a.name}**")
            st.image(get_identicon(hash_a), width=100, caption="Visual Hash Pattern")
            st.code(hash_a)

        with res_c2:
            st.markdown(f"**{file_b.name}**")
            st.image(get_identicon(hash_b), width=100, caption="Visual Hash Pattern")
            st.code(hash_b)
        
        # Kesimpulan
        if hash_a == hash_b:
            st.markdown("""
            <div class='result-box' style='background-color: rgba(76, 175, 80, 0.2); border: 2px solid #4CAF50;'>
                <h2 style='color: #4CAF50 !important;'>✅ MATCH!</h2>
                <p>Kedua file identik secara bit-per-bit.</p>
            </div>
            """, unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown("""
            <div class='result-box' style='background-color: rgba(230, 57, 70, 0.2); border: 2px solid #E63946;'>
                <h2 style='color: #E63946 !important;'>❌ MISMATCH!</h2>
                <p>Isi file berbeda. Perhatikan perbedaan pola gambar di atas.</p>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 2: FILE VS TEXT CODE
# =========================================================
with tab2:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.write("Cek integritas file hasil download dengan kode MD5 dari website.")
    
    col_up, col_inp = st.columns([1, 2])
    
    with col_up:
        file_check = st.file_uploader("Upload File", key="fc")
    
    with col_inp:
        md5_input = st.text_input("Paste Kode MD5 Asli:", placeholder="Contoh: 5d41402abc4b2a76b9719d911017c592")
    
    if file_check and md5_input:
        st.markdown("---")
        real_md5 = hitung_md5(file_check)
        target_md5 = md5_input.strip().lower()
        
        c1, c2, c3 = st.columns([2, 1, 2])
        
        with c1:
            st.caption("File Anda")
            st.code(real_md5)
        
        with c2:
            st.markdown("<h3 style='text-align: center; margin-top: 10px;'>VS</h3>", unsafe_allow_html=True)
            
        with c3:
            st.caption("Target Hash")
            st.code(target_md5)
            
        if real_md5 == target_md5:
            st.success("🎉 **VERIFIED**: File Valid dan Aman!")
        else:
            st.error("⚠️ **BAHAYA**: File Korup atau Telah Dimodifikasi!")
            
    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# TAB 3: TEKS GENERATOR
# =========================================================
with tab3:
    st.markdown("<div class='css-card'>", unsafe_allow_html=True)
    st.write("Ubah teks atau password menjadi hash MD5.")
    
    text_input = st.text_area("Masukkan Teks:", height=100, placeholder="Ketik sesuatu di sini...")
    
    if text_input:
        hashed_text = hash_string(text_input)
        
        st.markdown("### Hasil MD5:")
        st.code(hashed_text)
        
        col_viz, col_desc = st.columns([1, 4])
        with col_viz:
            st.image(get_identicon(hashed_text), width=80)
        with col_desc:
            st.info("Gambar di samping adalah representasi visual unik dari teks Anda. Ubah satu huruf saja, gambar akan berubah total.")
            
    st.markdown("</div>", unsafe_allow_html=True)
