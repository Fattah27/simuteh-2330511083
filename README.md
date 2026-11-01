# SIMUTEH — Evaluasi Praktikum P1-P4 Computer Vision

Mochammad Fattah Maulana Mansur | NIM 2330511083 | Kelas 7B | **SEED = 1083** (4 digit terakhir NIM)

Studi kasus: sistem bantu penilaian mutu daun teh (Sehat, Bercak Ringan, Bercak Berat) dari foto ponsel. Dataset sintetis bawaan (60 citra, 640x480) dibangkitkan dengan `src/buat_dataset_sintetis.py`.

## Struktur
- `notebook/` : B1_lingkungan, B2_citra_warna, B3_histogram, B4_penapisan, B5_praproses (.ipynb, keluaran tampak) + `Untitled0_lengkap.ipynb` (satu notebook utuh)
- `src/` : `buat_dataset_sintetis.py`, `utils_cv.py`, `praproses.py`
- `hasil/` : `param_praproses.json` dan gambar hasil
- `requirements.txt` : versi pustaka yang dipakai (OpenCV 4.14.0)

## Cara menjalankan (Google Colab)
1. Buka notebook di Colab, pilih Runtime > Restart sesi dan jalankan semua.
2. B2-B5 diawali sel *setup mandiri* yang menulis `src/` dan membangkitkan dataset (SEED 1083) bila belum ada, sehingga tiap notebook dapat dijalankan sendiri.
3. Lokal: `pip install -r requirements.txt`, lalu `python src/buat_dataset_sintetis.py` dari folder utama. Dataset (`data/`) tidak disertakan karena dapat dibuat ulang dengan SEED yang sama.

## Ringkasan hasil
- B2: kanal R paling memisahkan bercak (KB tertinggi di semua kondisi); bercak 5 mm perlu jarak <= 228 mm pada foto 640 px.
- B3: pilihan perbaikan per kondisi (gelap: gamma 0,5; terang: gamma 1,8; kontras rendah: regang persentil 2-98; bayangan: CLAHE). KB bukan satu-satunya ukuran; sebagian pilihan menurunkan KB namun lebih benar secara visual.
- B4: konvolusi manual identik dengan `filter2D` (selisih 0); median 5x5 terbaik untuk derau bawaan (PSNR rerata 41,04 dB pada 12 citra normal); kernel median >= 9 melemahkan bercak kecil.
- B5: rangkaian praproses final (lebar 640, gamma 1,0, CLAHE clip 1,0 tile 8 pada kanal V, median 5, tanpa penajaman) menaikkan KB di kelima kondisi (+33,8% sampai +97,1%); simpangan baku daun sehat turun di semua kondisi (tidak ada bercak palsu).

## Catatan
Alat bantu AI (Claude) dipakai untuk memahami konsep dan memeriksa kode; lihat bagian Refleksi laporan.
"# simuteh-2330511083" 
