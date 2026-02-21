# veri_uret_calistir.py
from veri_uret import csv_uret_staj_verileri_formatinda

csv_uret_staj_verileri_formatinda(
    ogrenci_sayisi=120,
    firma_sayisi=50,
    tercih_sayisi=5,
    dosya_adi="uretilenStajVerileri.csv",
    seed=42
)

print("uretilenStajVerileri.csv üretildi.")
