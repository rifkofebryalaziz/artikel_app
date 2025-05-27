# --- Konfigurasi Halaman Harus Paling Atas ---
import streamlit as st
st.set_page_config(
    page_title="Visualisasi Artikel Basket",
    layout="wide",
    page_icon="🏀"
)

# --- Library Tambahan ---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from wordcloud import WordCloud
import re
from collections import Counter
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# --- Judul ---
st.title("Visualisasi Artikel Basket dari detik.com")

# --- Load Data ---
@st.cache_data
def load_data():
    try:
        MONGO_URI = "mongodb+srv://rifkofebryalaziz30:phb_2022_rifkofebryalaziz_TI@cluster0.qotuptw.mongodb.net/detik?retryWrites=true&w=majority"
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()
        db = client["detik"]
        collection = db["baskett_articless"]
        data = list(collection.find())
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        st.error(f"Gagal koneksi MongoDB: {e}")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Data tidak ditemukan.")
    st.stop()

# --- Stopwords ---
stopword_factory = StopWordRemoverFactory()
stopwords = set(stopword_factory.get_stop_words())
custom_stopwords = {
    'kata', 'salah', 'tersebut', 'jadi', 'hingga', 'tak', 'tidak', 'yang', 'untuk',
    'dari', 'oleh', 'dalam', 'atas', 'sudah', 'akan', 'ini', 'itu', 'sangat', 'juga',
    'lalu', 'baru', 'pun', 'semua', 'apa', 'kalau', 'kini', 'mungkin', 'namun',
    'memang', 'tetap', 'agar', 'bukan', 'dengan', 'telah', 'adalah', 'sendiri', 'atau',
    'satu', 'sama', 'lebih', 'bagaimana', 'terus', 'melalui', 'punya', 'masih', 'sejak',
    'baik', 'bahkan', 'selama', 'ketika', 'kemudian', 'sedang', 'karena', 'bahwa',
    'berikut', 'sebelum', 'setelah', 'antara', 'sebagai', 'yaitu', 'setiap'
}
stopwords.update(custom_stopwords)

def preprocess_text(text_series):
    text = ' '.join(text_series.dropna().astype(str)).lower()
    words = re.findall(r'\b\w+\b', text)
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)

# --- Statistik Artikel ---
st.subheader("Statistik Artikel")

bulan_mapping = {
    'Januari': '01', 'Februari': '02', 'Maret': '03', 'April': '04',
    'Mei': '05', 'Juni': '06', 'Juli': '07', 'Agustus': '08',
    'September': '09', 'Oktober': '10', 'November': '11', 'Desember': '12'
}

def bersihkan_tanggal(tanggal_str):
    try:
        tanggal_str = re.sub(r'^[A-Za-z]+,\s*', '', tanggal_str)
        tanggal_str = re.sub(r'\s*WIB', '', tanggal_str)
        tanggal_str = tanggal_str.strip()
        for nama_bulan, angka in bulan_mapping.items():
            if nama_bulan in tanggal_str:
                tanggal_str = tanggal_str.replace(nama_bulan, angka)
                break
        return pd.to_datetime(tanggal_str, format='%d %m %Y %H:%M')
    except:
        return pd.NaT

df['tanggal_bersih'] = df['tanggal'].astype(str).apply(bersihkan_tanggal)
valid_tanggal_df = df.dropna(subset=['tanggal_bersih'])

total_artikel = len(df)
st.markdown(f"- **Total Artikel:** {total_artikel}")

if not valid_tanggal_df.empty:
    tanggal_terlama = valid_tanggal_df['tanggal_bersih'].min().date()
    tanggal_terbaru = valid_tanggal_df['tanggal_bersih'].max().date()
    st.markdown(f"- **Rentang Waktu Publikasi Berita:** {tanggal_terlama} hingga {tanggal_terbaru}")
else:
    st.info("Tidak ada data tanggal yang valid untuk dihitung rentang waktunya.")

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Word Cloud Isi Artikel ---
st.subheader("Word Cloud Isi Artikel")
cleaned_isi = preprocess_text(df['isi'])
wc_isi = WordCloud(width=1200, height=800, background_color='white').generate(cleaned_isi)
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.imshow(wc_isi, interpolation='bilinear')
ax1.axis('off')
st.pyplot(fig1)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Word Cloud Judul Artikel ---
st.subheader("Word Cloud Judul Artikel")
cleaned_judul = preprocess_text(df['judul'])
wc_judul = WordCloud(width=1200, height=800, background_color='white').generate(cleaned_judul)
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.imshow(wc_judul, interpolation='bilinear')
ax2.axis('off')
st.pyplot(fig2)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Top 15 Kata Judul ---
st.subheader("Top 15 Kata di Judul Artikel")
top_words = Counter(cleaned_judul.split()).most_common(15)
words, counts = zip(*top_words)
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x=list(counts), y=list(words), ax=ax3)
ax3.set_xlabel("Frekuensi")
ax3.set_ylabel("Kata")
st.pyplot(fig3)

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Daftar Artikel ---
st.subheader("Daftar Artikel")
if {'judul', 'isi', 'link', 'tanggal'}.issubset(df.columns):
    df_table = df[['judul', 'isi', 'tanggal', 'link']].fillna('-').head(3000)
    df_table.index += 1
    st.dataframe(df_table, use_container_width=True)
else:
    st.warning("Kolom 'judul', 'isi', 'tanggal', atau 'link' tidak ditemukan di data.")

st.markdown("<br><br>", unsafe_allow_html=True)

# --- Pencarian Artikel ---
st.subheader("Pencarian Artikel")
search_query = st.text_input("Masukkan kata kunci untuk mencari judul:")
if search_query:
    hasil_cari = df[df['judul'].str.contains(search_query, case=False, na=False)]
    st.write(f"Ditemukan {len(hasil_cari)} artikel:")
    st.dataframe(hasil_cari[['judul', 'isi', 'tanggal', 'link']].fillna('-'), use_container_width=True)
