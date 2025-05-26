import streamlit as st

st.set_page_config(layout="wide")
st.title("Visualisasi Artikel Basket dari Detik.com")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from wordcloud import WordCloud
import re
from collections import Counter

# Tambahan untuk stopword dari Sastrawi
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# Koneksi ke Mongodb
@st.cache_data
def load_data():
    try:
        client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
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

# Gabungan stopword dari Sastrawi dan manual
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

# Fungsi preprocessing
def preprocess_text(text_series):
    text = ' '.join(text_series.dropna().astype(str)).lower()
    words = re.findall(r'\b\w+\b', text)
    filtered_words = [word for word in words if word not in stopwords]
    return ' '.join(filtered_words)

# Word Cloud Isi Artikel
st.subheader("Word Cloud Isi Artikel")
cleaned_isi = preprocess_text(df['isi'])
wc_isi = WordCloud(width=1200, height=800, background_color='white').generate(cleaned_isi)
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.imshow(wc_isi, interpolation='bilinear')
ax1.axis('off')
st.pyplot(fig1)

# Word Cloud Judul Artikel
st.subheader("Word Cloud Judul Artikel")
cleaned_judul = preprocess_text(df['judul'])
wc_judul = WordCloud(width=1200, height=800, background_color='white').generate(cleaned_judul)
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.imshow(wc_judul, interpolation='bilinear')
ax2.axis('off')
st.pyplot(fig2)

# Top 15 Kata di Judul Artikel
st.subheader("Top 15 Kata di Judul Artikel")
top_words = Counter(cleaned_judul.split()).most_common(15)
words, counts = zip(*top_words)
fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.barplot(x=list(counts), y=list(words), ax=ax3)
ax3.set_xlabel("Frekuensi")
ax3.set_ylabel("Kata")
st.pyplot(fig3)

# Tabel Judul, Isi, Tanggal, dan Link dengan Tampilan Modern
st.subheader("Tabel Artikel: Judul, Isi, Tanggal, dan Link")

if {'judul', 'isi', 'link', 'tanggal'}.issubset(df.columns):
    df_table = df[['judul', 'isi', 'tanggal', 'link']].fillna('-').head(3000)
    df_table.index += 1  # Mulai nomor dari 1
    st.dataframe(df_table, use_container_width=True)
else:
    st.warning("Kolom 'judul', 'isi', 'tanggal', atau 'link' tidak ditemukan di data.")

# BONUS: Fitur Pencarian Judul Artikel
st.subheader("Pencarian Judul Artikel")
search_query = st.text_input("Masukkan kata kunci untuk mencari judul:")
if search_query:
    hasil_cari = df[df['judul'].str.contains(search_query, case=False, na=False)]
    st.write(f"Ditemukan {len(hasil_cari)} artikel:")
    st.dataframe(hasil_cari[['judul', 'tanggal', 'link']])
