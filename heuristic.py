import time
import random

def heuristic_ata(ogrenciler_master, firmalar_master, red_orani):
    start = time.perf_counter()
    ogrenciler = [o.copy() for o in ogrenciler_master]
    kontenjanlar = firmalar_master.copy()
    tur, islemler = 0, 0
    

    populerlik_sozlugu = {}
    for ogr in ogrenciler:
        for tercih in ogr['tercihler']:
            populerlik_sozlugu[tercih] = populerlik_sozlugu.get(tercih, 0) + 1

    while tur < 250:
        tur += 1
        yerlesmemisler = [o for o in ogrenciler if o['durum'] == 'Yerlesmedi']
        if not yerlesmemisler: break
        
        # --- ESKİ FORMÜLÜN YENİ KODA UYARLANMASI ---
        for o in yerlesmemisler:
            # Öğrencinin tercihlerinin ortalama popülerliğini hesapla
            toplam_talep = sum(populerlik_sozlugu.get(t, 0) for t in o['tercihler'])
            ortalama_talep = toplam_talep / len(o['tercihler']) if o['tercihler'] else 0
            
            # Formül: GNO Ağırlığı + Popülerlik Etkisi + Küçük Rastgelelik
            # Bu skor, popüler yerleri isteyen yüksek puanlılara öncelik vererek tıkanmayı önler.
            o['h_skor'] = (o['gno'] * 2.0) + (ortalama_talep * 0.05) + random.uniform(-0.1, 0.1)
        
        # Yeni h_skor değerine göre sırala
        yerlesmemisler.sort(key=lambda x: x['h_skor'], reverse=True)
        
        # --- YERLEŞTİRME SÜRECİ ---
        for ogr in yerlesmemisler:
            islemler += 1
            atanabildi = False
            for idx, t in enumerate(ogr['tercihler']):
                if kontenjanlar.get(t, 0) > 0:
                    ogr['yerlestigi_firma'] = t
                    ogr['durum'] = 'Onerildi'
                    ogr['tercih_no'] = idx + 1
                    kontenjanlar[t] -= 1
                    atanabildi = True
                    break
            
            if not atanabildi:
                boslar = [f for f, k in kontenjanlar.items() if k > 0]
                if boslar:
                    s = random.choice(boslar)
                    ogr['yerlestigi_firma'] = s
                    ogr['durum'] = 'Onerildi'
                    ogr['tercih_no'] = "Rastgele"
                    kontenjanlar[s] -= 1
        
        # --- RED SİMÜLASYONU ---
        for ogr in ogrenciler:
            if ogr['durum'] == 'Onerildi':
                if random.random() < red_orani:
                    kontenjanlar[ogr['yerlestigi_firma']] += 1
                    ogr['yerlestigi_firma'] = None
                    ogr['durum'] = 'Yerlesmedi'
                else:
                    ogr['durum'] = 'Yerlestirildi'
                
    return {
        "tur": tur, 
        "liste": ogrenciler, 
        "sure": time.perf_counter() - start, 
        "islem": islemler
    }