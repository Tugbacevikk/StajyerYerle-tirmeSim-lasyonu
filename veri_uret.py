# veri_uret.py
import pandas as pd
import numpy as np

def csv_uret_staj_verileri_formatinda(
    ogrenci_sayisi=120,
    firma_sayisi=50,
    tercih_sayisi=5,
    min_kontenjan=1,
    max_kontenjan=5,
    min_gno=2.00,
    max_gno=4.00,
    seed=42,
    dosya_adi="uretilenStajVerileri.csv"
):
    rng = np.random.default_rng(seed)

    # 1) Firma listesi
    firmalar = [f"Firma_{i+1}" for i in range(firma_sayisi)]
    kontenjanlar = rng.integers(min_kontenjan, max_kontenjan + 1, size=firma_sayisi).astype(int)

    # 2) Öğrenciler
    ogr_ids = [f"Ogr{str(i+1).zfill(3)}" for i in range(ogrenci_sayisi)]
    gno_vals = np.round(rng.uniform(min_gno, max_gno, size=ogrenci_sayisi), 2)
    gno_str = [f"{x:.2f}".replace(".", ",") for x in gno_vals]

    # 3) Tercihler (Sadece firmaların içinden)
    firmalar_np = np.array(firmalar, dtype=object)
    tercih_listeleri = []
    for _ in range(ogrenci_sayisi):
        perm = rng.permutation(firmalar_np)
        tercih = perm[:tercih_sayisi]
        tercih_listeleri.append(",".join(tercih.tolist()))

    # 4) Şablon: satır sayısı
    n = max(firma_sayisi, ogrenci_sayisi)

    # 5) Kolonları n uzunluğunda hazırla
    firm_col = [np.nan] * n
    kont_col = [np.nan] * n
    ogr_col = [np.nan] * n
    tercih_col = [np.nan] * n
    gno_col = [np.nan] * n

    # Firmaları ilk firma_sayisi satıra yerleştir
    for i in range(firma_sayisi):
        firm_col[i] = firmalar[i]
        kont_col[i] = int(kontenjanlar[i])

    # Öğrencileri ilk ogrenci_sayisi satıra yerleştir
    for i in range(ogrenci_sayisi):
        ogr_col[i] = ogr_ids[i]
        tercih_col[i] = tercih_listeleri[i]
        gno_col[i] = gno_str[i]

    df = pd.DataFrame({
        "Firmalar": firm_col,
        "Kontenjanlar": kont_col,
        "Unnamed: 2": [np.nan] * n,
        "Unnamed: 3": [np.nan] * n,
        "Unnamed: 4": [np.nan] * n,
        "Öğrenci": ogr_col,
        "Tercih Sırası": tercih_col,
        "GNO": gno_col
    })

    df.to_csv(dosya_adi, sep=";", index=False, encoding="iso-8859-9")
    return dosya_adi
