import time
import random

def greedy_ata(ogrenciler_master, firmalar_master, red_orani):
    start = time.perf_counter()
    ogrenciler = [o.copy() for o in ogrenciler_master]
    kontenjanlar = firmalar_master.copy()
    tur, islemler = 0, 0
    
    while tur < 250:
        tur += 1
        yerlesmemisler = [o for o in ogrenciler if o['durum'] == 'Yerlesmedi']
        if not yerlesmemisler: break
        
        # Greedy: GNO'ya göre kesin sıralama
        yerlesmemisler.sort(key=lambda x: x['gno'], reverse=True)
        
        for ogr in yerlesmemisler:
            islemler += 1
            atanabildi = False
            for idx, t in enumerate(ogr['tercihler']):
                if kontenjanlar.get(t, 0) > 0:
                    ogr['yerlestigi_firma'] = t; ogr['durum'] = 'Onerildi'
                    ogr['tercih_no'] = idx + 1
                    kontenjanlar[t] -= 1; atanabildi = True; break
            if not atanabildi:
                boslar = [f for f, k in kontenjanlar.items() if k > 0]
                if boslar:
                    s = random.choice(boslar); ogr['yerlestigi_firma'] = s
                    ogr['durum'] = 'Onerildi'; ogr['tercih_no'] = "Rastgele"; kontenjanlar[s] -= 1
        
        for ogr in ogrenciler:
            if ogr['durum'] == 'Onerildi':
                if random.random() < red_orani:
                    kontenjanlar[ogr['yerlestigi_firma']] += 1
                    ogr['yerlestigi_firma'] = None; ogr['durum'] = 'Yerlesmedi'
                else: ogr['durum'] = 'Yerlestirildi'
    
    return {"tur": tur, "liste": ogrenciler, "sure": time.perf_counter()-start, "islem": islemler}