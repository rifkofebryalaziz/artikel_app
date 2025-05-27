# import requests as req
# from bs4 import BeautifulSoup as bs
# from datetime import datetime
# from pymongo import MongoClient
# import time

# # Koneksi ke MongoDB
# client = MongoClient('mongodb://localhost:27017')  # Ubah jika kamu pakai Atlas atau URI lain
# db = client['detik']  # Sesuai nama database
# collection = db['basket_articless']  # Nama koleksi

# # Header request
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
# }

# def scrape_detik(jumlah_halaman):
#     a = 1
#     for page in range(1, jumlah_halaman + 1):
#         try:
#             print(f"\n[INFO] Scraping halaman {page}")
#             url = f'https://www.detik.com/search/searchall?query=Basket&siteid=2&source_kanal=true&page={page}'
#             res = req.get(url, headers=headers)
#             soup = bs(res.text, 'html.parser')
#             articles = soup.find_all('article', class_='list-content__item')

#             if not articles:
#                 print(f"Halaman {page} tidak ditemukan atau kosong.")
#                 continue

#             for article in articles:
#                 try:
#                     a_tag = article.find('h3', class_='media__title').find('a')
#                     if not a_tag or 'href' not in a_tag.attrs:
#                         continue
#                     link = a_tag['href']
#                     title = a_tag.get_text(strip=True)

#                     date_tag = article.find('div', class_='media__date').find('span') if article.find('div', class_='media__date') else None
#                     date = date_tag['title'] if date_tag else 'Tanggal tidak ditemukan'

#                     try:
#                         parsed_date = datetime.strptime(date, "%A, %d %b %Y %H:%M WIB")
#                     except:
#                         print(f"Format tanggal tidak valid: {date}")
#                         parsed_date = None

#                     detail_page = req.get(link, headers=headers)
#                     detail_soup = bs(detail_page.text, 'html.parser')
#                     body = detail_soup.find_all('div', class_='detail__body-text itp_bodycontent')

#                     if not body:
#                         continue

#                     content = ''
#                     for section in body:
#                         paragraphs = section.find_all('p')
#                         content += ''.join(p.get_text(strip=True) for p in paragraphs)

#                     content = content.replace('ADVERTISEMENT', '').replace('SCROLL TO RESUME CONTENT', '').replace('\n', '')

#                     if collection.find_one({'link': link}):
#                         print(f"Data sudah ada: {title[:40]}...")
#                         continue

#                     document = {
#                         'judul': title,
#                         'tanggal': parsed_date,
#                         'link': link,
#                         'isi': content
#                     }
#                     collection.insert_one(document)
#                     print(f'done[{a}] > {title[:40]}...')
#                     a += 1

#                 except Exception as e:
#                     print(f"[Error Artikel] {e}")

#             time.sleep(1)  # ⏱️ Jeda aman 1 detik antara halaman

#         except Exception as e:
#             print(f"[Error Halaman] Halaman {page}: {e}")

# # Jalankan scraping 415 halaman
# scrape_detik(415)





# import requests as req
# from bs4 import BeautifulSoup as bs
# from datetime import datetime
# from pymongo import MongoClient
# import time

# # Koneksi ke MongoDB
# client = MongoClient('mongodb://localhost:27017')  # Ubah jika pakai URI lain
# db = client['detik']  # Nama database
# collection = db['baskett_articless']  # Nama koleksi

# # Header request
# headers = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
# }

# def scrape_detik(jumlah_halaman):
#     a = 1
#     for page in range(1, jumlah_halaman + 1):
#         try:
#             print(f"\n[INFO] Scraping halaman {page}")
#             url = f'https://www.detik.com/search/searchall?query=Basket&siteid=2&source_kanal=true&page={page}'
#             res = req.get(url, headers=headers)
#             soup = bs(res.text, 'html.parser')
#             articles = soup.find_all('article', class_='list-content__item')

#             if not articles:
#                 print(f"Halaman {page} tidak ditemukan atau kosong.")
#                 continue

#             for article in articles:
#                 try:
#                     a_tag = article.find('h3', class_='media__title').find('a')
#                     if not a_tag or 'href' not in a_tag.attrs:
#                         continue
#                     link = a_tag['href']
#                     title = a_tag.get_text(strip=True)

#                     # Ambil tanggal asli dari atribut 'title', jika ada
#                     date_tag = article.find('div', class_='media__date').find('span') if article.find('div', class_='media__date') else None
#                     date_raw = date_tag['title'] if date_tag and date_tag.has_attr('title') else 'Tanggal tidak ditemukan'

#                     # Validasi parsing tanggal (tidak dipakai sebagai data utama)
#                     try:
#                         datetime.strptime(date_raw, "%A, %d %b %Y %H:%M WIB")
#                     except:
#                         print(f"Format tanggal tidak valid atau tidak ditemukan: {date_raw}")

#                     # Ambil isi artikel
#                     detail_page = req.get(link, headers=headers)
#                     detail_soup = bs(detail_page.text, 'html.parser')
#                     body = detail_soup.find_all('div', class_='detail__body-text itp_bodycontent')

#                     if not body:
#                         continue

#                     content = ''
#                     for section in body:
#                         paragraphs = section.find_all('p')
#                         content += ''.join(p.get_text(strip=True) for p in paragraphs)

#                     content = content.replace('ADVERTISEMENT', '').replace('SCROLL TO RESUME CONTENT', '').replace('\n', '')

#                     # Cek apakah sudah ada datanya
#                     if collection.find_one({'link': link}):
#                         print(f"Data sudah ada: {title[:40]}...")
#                         continue

#                     # Simpan ke MongoDB dengan tanggal mentah (string)
#                     document = {
#                         'judul': title,
#                         'tanggal': date_raw,
#                         'link': link,
#                         'isi': content
#                     }
#                     collection.insert_one(document)
#                     print(f'done[{a}] > {title[:40]}...')
#                     a += 1

#                 except Exception as e:
#                     print(f"[Error Artikel] {e}")

#             time.sleep(1)  # ⏱️ Jeda aman 1 detik antara halaman

#         except Exception as e:
#             print(f"[Error Halaman] Halaman {page}: {e}")

# # Jalankan scraping
# scrape_detik(417)

import requests as req
from bs4 import BeautifulSoup as bs
from datetime import datetime
from pymongo import MongoClient
import time

# Koneksi ke MongoDB
client = MongoClient('mongodb://localhost:27017')  # Ubah jika pakai URI lain
db = client['detik']  # Nama database
collection = db['baskett_articless']  # Nama koleksi

# Header request
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'
}

def scrape_detik(start_page, end_page):
    a = 1
    for page in range(start_page, end_page + 1):
        try:
            print(f"\n[INFO] Scraping halaman {page}")
            url = f'https://www.detik.com/search/searchall?query=Basket&siteid=2&source_kanal=true&page={page}'
            res = req.get(url, headers=headers)
            soup = bs(res.text, 'html.parser')
            articles = soup.find_all('article', class_='list-content__item')

            if not articles:
                print(f"Halaman {page} tidak ditemukan atau kosong.")
                continue

            for article in articles:
                try:
                    a_tag = article.find('h3', class_='media__title').find('a')
                    if not a_tag or 'href' not in a_tag.attrs:
                        continue
                    link = a_tag['href']
                    title = a_tag.get_text(strip=True)

                    date_tag = article.find('div', class_='media__date').find('span') if article.find('div', class_='media__date') else None
                    date_raw = date_tag['title'] if date_tag and date_tag.has_attr('title') else 'Tanggal tidak ditemukan'

                    try:
                        datetime.strptime(date_raw, "%A, %d %b %Y %H:%M WIB")
                    except:
                        print(f"Format tanggal tidak valid atau tidak ditemukan: {date_raw}")

                    detail_page = req.get(link, headers=headers)
                    detail_soup = bs(detail_page.text, 'html.parser')
                    body = detail_soup.find_all('div', class_='detail__body-text itp_bodycontent')

                    if not body:
                        continue

                    content = ''
                    for section in body:
                        paragraphs = section.find_all('p')
                        content += ''.join(p.get_text(strip=True) for p in paragraphs)

                    content = content.replace('ADVERTISEMENT', '').replace('SCROLL TO RESUME CONTENT', '').replace('\n', '')

                    if collection.find_one({'link': link}):
                        print(f"Data sudah ada: {title[:40]}...")
                        continue

                    document = {
                        'judul': title,
                        'tanggal': date_raw,
                        'link': link,
                        'isi': content
                    }
                    collection.insert_one(document)
                    print(f'done[{a}] > {title[:40]}...')
                    a += 1

                except Exception as e:
                    print(f"[Error Artikel] {e}")

            time.sleep(1)

        except Exception as e:
            print(f"[Error Halaman] Halaman {page}: {e}")

# Jalankan scraping dari halaman 316 sampai 417
scrape_detik(316, 417)
