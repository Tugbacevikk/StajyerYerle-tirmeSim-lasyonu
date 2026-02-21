import pandas as pd
import numpy as np
import time
import random
import tkinter as tk
from tkinter import messagebox, ttk

# DIŞARIDAN GELEN YARDIMCILAR 
# yazdığımız özel algoritmaları buradan içeri alıyoruz
from greedy import greedy_ata
from heuristic import heuristic_ata

#  SİSTEM AYARLARI 
# %20 ihtimalle şirketlerin stajyeri reddettiği oran 
RED_ORANI = 0.2 
# default olarak giriş atandı
GIRIS_BILGILERI = {"kullanici": "akademisyen", "sifre": "1234"}

# ARKA PLAN İŞLERİ 
class StajSimulasyonu:
    def __init__(self, dosya_yolu):
        self.dosya_yolu = dosya_yolu # dışarıdan gelen dosya yolu nesnenin kendi içine kaydedildi
        self.ogrenciler_master = []  # liste kullanıldı çünkü öğrencileri başarı puanına göre sıralanacak
        self.firmalar_master = {}  # firmaları ve kontenjanlarını saklamak için boş bir sözlük açıldı

    def veriyi_yukle(self):
        try:
            # dosya okundu ve sütunlardaki boşluklar temizlendi
            df = pd.read_csv(self.dosya_yolu, sep=';', encoding='iso-8859-9')
            df.columns = [c.strip() for c in df.columns]
            
            # şirketler ve kontenjanları sözlük yapısına alındı
            firma_df = df[['Firmalar', 'Kontenjanlar']].dropna()
            self.firmalar_master = {row.Firmalar: int(row.Kontenjanlar) for row in firma_df.itertuples()}
            
            # öğrenci listesini hazırlandı
            self.ogrenciler_master = []
            ogr_df = df[['Öğrenci', 'Tercih Sırası', 'GNO']].dropna()
            
            # gno'daki virgüller noktaya çevrilip sayıya dönüştürüldü
            if ogr_df['GNO'].dtype == object:
                ogr_df['GNO'] = ogr_df['GNO'].str.replace(',', '.').astype(float)
            
            # her öğrenci birer sözlük objesi olarak listeye eklendi
            for row in ogr_df.itertuples(): # her satır bir nesneye dönüştürülerek gno ve öğrencilere erişildi
                tercihler = [t.strip() for t in str(getattr(row, '_2')).split(',')]
                self.ogrenciler_master.append({
                    'id': str(row.Öğrenci), 'tercihler': tercihler,
                    'gno': row.GNO, 'yerlestigi_firma': None, 'durum': 'Yerlesmedi'
                })
            return True
        except Exception as e:
            messagebox.showerror("Hata", f"Veri yüklenemedi: {e}")
            return False

    def calistir(self, yontem="Greedy"):
        # guiden gelen istek üzerine istenen algoritma çalıştırıldı
        if yontem == "Greedy":
            return greedy_ata(self.ogrenciler_master, self.firmalar_master, RED_ORANI)
        else:
            return heuristic_ata(self.ogrenciler_master, self.firmalar_master, RED_ORANI)


# GÖRSEL ARAYÜZ KISMI
class UygulamaGUI:
    def __init__(self, root):
        # ana pencere ayarları
        self.root = root
        self.root.title("Staj Atama Sistemi - Akademisyen Paneli")
        self.root.geometry("1200x850")
        self.root.configure(bg="#ecf0f1")

    
        #veri yükleme: istenilen dataset değiştirilebilir
        self.sim = StajSimulasyonu("uretilenStajVerileri.csv")
        self.sonuclar = {}
        
        # her şeyi içine koyacağımız ana kutu
        self.main_container = tk.Frame(self.root, bg="#ecf0f1")
        self.main_container.pack(fill="both", expand=True)
        self.giris_ekranini_olustur()

    # EKRANLAR VE GÖRÜNÜMLER 

    def giris_ekranini_olustur(self):
        
        # ekranlar arası geçiş yaparken ana taşıyıcı içindeki eski görseller temizlendi
        for widget in self.main_container.winfo_children(): 
            widget.destroy()
        
        # tüm ekranı kaplayan koyu mavi tonlarında ana giriş çerçevesi
        login_frame = tk.Frame(self.main_container, bg="#34495e")
        login_frame.pack(fill="both", expand=True)
        
        # ekranın tam ortasına yerleşen, kenarlıkları vurgulanmış giriş formu kutusu
        form_box = tk.Frame(login_frame, bg="#2c3e50", padx=50, pady=50, highlightbackground="#3498db", highlightthickness=2)
        form_box.place(relx=0.5, rely=0.5, anchor="center") # relx ve rely 0.5 ile tam merkezleme yapıldı
        
        # formun en üstündeki başlık etiketi
        tk.Label(form_box, text="AKADEMİSYEN GİRİŞİ", font=("Arial", 18, "bold"), fg="white", bg="#2c3e50").pack(pady=(0, 30))
        
        # kullanıcı adı (akademisyen) ayarlandı
        tk.Label(form_box, text="Akademisyen Adı:", fg="#bdc3c7", bg="#2c3e50", font=("Arial", 10)).pack(anchor="w")
        self.ent_user = tk.Entry(form_box, font=("Arial", 12), width=25)
        self.ent_user.pack(pady=(5, 15))
        self.ent_user.insert(0, "akademisyen") # geliştirme sürecinde kolaylık olması için varsayılan değer olarak eklendi
        
        # default oarak da belirtilen şifre alanı
        tk.Label(form_box, text="Şifre:", fg="#bdc3c7", bg="#2c3e50", font=("Arial", 10)).pack(anchor="w")
        self.ent_pass = tk.Entry(form_box, show="*", font=("Arial", 12), width=25) # karakterler yıldız (*) olarak gizlendi
        self.ent_pass.pack(pady=(5, 30))
        
        # giriş butonu
        # tıklandığında 'self.giris_kontrol' fonksiyonuna onay butonu
        tk.Button(form_box, text="SİSTEME GİRİŞ YAP", command=self.giris_kontrol, 
                  bg="#27ae60", fg="white", font=("Arial", 11, "bold"), padx=20, pady=10).pack(fill="x")

    def ana_paneli_olustur(self):
        #giriş başarılıysa açılan tüm analizlerin ve tabloların olduğu ana ekranı kurar 
        
        # ekran değiştiği için içindeki her şey temizlendi
        for widget in self.main_container.winfo_children(): 
            widget.destroy()
        
       
        # sayfanın en üstünde butonların ve arama çubuğunun duracağı koyu renkli şerit
        toolbar = tk.Frame(self.main_container, pady=10, bg="#2c3e50")
        toolbar.pack(fill="x")
        
        # simülasyonu başlatan yeşil başlat butonu
        tk.Button(toolbar, text=" SİMÜLASYONU BAŞLAT", command=self.hesapla, 
                  bg="#2ecc71", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=15)
        
        # ogrenci idsine göre arama bölümü
        tk.Label(toolbar, text="Öğrenci Ara (ID):", bg="#2c3e50", fg="white", font=("Arial", 10)).pack(side="left", padx=(20, 5))
        
        # arama kutusuna her harf yazıldığında filtreleme fonksiyonunu çalıştırır
        # gerçek hayat aplikasyonlarına benzerlik taşıyan bir yönüdür.
        self.search_var = tk.StringVar() 
        self.search_var.trace_add("write", self.tabloyu_filtrele)
        self.search_entry = tk.Entry(toolbar, textvariable=self.search_var, font=("Arial", 10))
        self.search_entry.pack(side="left", padx=5)
        
        # sisteme baştan geri dönmeyi sağlayan kırmızı çıkış butonu
        tk.Button(toolbar, text=" GÜVENLİ ÇIKIŞ", command=self.guvenli_cikis, 
                  bg="#e74c3c", fg="white", font=("Arial", 10, "bold")).pack(side="right", padx=15)
        
        # orta alan ayarlaması
        # kullanıcının fareyle sağa-sola çekerek boyutlandırabileceği iki bölmeli alan
        self.panes = tk.PanedWindow(self.main_container, orient="horizontal", bg="#bdc3c7", sashwidth=4)
        self.panes.pack(fill="both", expand=True, padx=10, pady=10)
        
        # sol bölme Greedy algoritması sonuçları için çerçeve olarak ayarlandı
        self.frame_g = tk.LabelFrame(self.panes, text="Greedy (Başarı Sıralı)", font=("Arial", 10, "bold"), fg="#2c3e50")
        # sağ bölme Heuristic algoritması sonuçları için çerçeve olarak ayarlandı
        self.frame_h = tk.LabelFrame(self.panes, text="Heuristic (Esnek Yaklaşım)", font=("Arial", 10, "bold"), fg="#2c3e50")
        
        # çerçeveler bölmeli alana eklendi
        self.panes.add(self.frame_g, stretch="always")
        self.panes.add(self.frame_h, stretch="always")
        
        # tablo_yap kullanarak iki algoritma için de boş listeler oluşturuldu
        self.tree_g = self.tablo_yap(self.frame_g)
        self.tree_h = self.tablo_yap(self.frame_h)
        
        # alt bilgi ve kontrol çubuğu
        # sayfanın en altında rapor butonlarının duracağı açık renkli alan
        self.control_panel = tk.Frame(self.main_container, bg="#ecf0f1", height=100, pady=10)
        self.control_panel.pack(fill="x", side="bottom")
        
        # sistemin durumu hakkında kullanıcıya mesaj veren etiket
        self.lbl_info = tk.Label(self.control_panel, text="Sistem Hazır.", font=("Arial", 10), bg="#ecf0f1")
        self.lbl_info.pack(side="left", padx=20)
        
        # rapor ve analiz butonları başlangıçta  'disabled' dururlar hesaplama bitince açılırlar
        self.btn_report = tk.Button(self.control_panel, text=" FİNAL RAPORU", command=self.final_raporu_ekranı, 
                                    bg="#3498db", fg="white", font=("Arial", 10, "bold"), state="disabled")
        self.btn_report.pack(side="right", padx=10)
        
        self.btn_step = tk.Button(self.control_panel, text=" ADIM ADIM ANALİZ", command=self.adim_adim_ekranı, 
                                   bg="#e67e22", fg="white", font=("Arial", 10, "bold"), state="disabled")
        self.btn_step.pack(side="right", padx=10)

        # kullanıcı rapor veya analiz yaptırıp geri dönüğünde analiz bilgilerinin sabit kalması için taarlandı bu sayede 
        # adım adım analiz ve final raporu birbiri ile uyumlu oldu
        if self.sonuclar:
            self.tablolari_doldur() # Eski verileri tablolara yaz
            self.btn_report.config(state="normal") # Rapor butonlarını tekrar aktif et
            self.btn_step.config(state="normal")
            self.lbl_info.config(text=" Mevcut sonuçlar yüklendi.", fg="#2980b9")



    def tablo_yap(self, parent_frame):
        # öğrencileri listeleyeceğimiz tabloları oluşturan  metot
        
        # tablo çok uzun olduğunda aşağı kaydırabilmek için bir kaydırma çubuğu oluşturduk
        # 'side="right"' ile sağa yaslıyoruz, 'fill="y"' ile dikeyde tam boy uzattık
        scrolly = tk.Scrollbar(parent_frame); scrolly.pack(side="right", fill="y")
        
        # 'columns' ile sütun başlıklarını tanımladık
        # 'show="headings"' diyerek en baştaki boş sütununu gizledik
        t = ttk.Treeview(parent_frame, columns=("ID", "GNO", "Firma", "Sira"), show="headings", yscrollcommand=scrolly.set)
        
        # tablonun en üstünde görünecek başlık yazılarını belirledik
        t.heading("ID", text="Öğrenci ID")
        t.heading("GNO", text="GNO")
        t.heading("Firma", text="Yerleştiği Şirket")
        t.heading("Sira", text="Tercih Sırası")
        
        # width: Sütunun genişliği
        # anchor: Metnin hizalaması yapıldı
        t.column("ID", width=100, anchor="center")
        t.column("GNO", width=50, anchor="center")
        t.column("Firma", width=150, anchor="w")
        t.column("Sira", width=80, anchor="center")
        
        # tabloya veri eklerken tag kullanarak satırları renklendirdik
        # 'birinci': Öğrenci 1. tercihine yerleştiyse yeşil arka plan yapıldı
        t.tag_configure('birinci', foreground='white', background='#27ae60')
        # 'diger_tercih': 2., 3. veya sonraki tercihlerine yerleştiyse mavi yapıldı
        t.tag_configure('diger_tercih', foreground='white', background='#3498db')
        # 'liste_disi': Tercihlerinden hiçbirine giremeyip rastgele atandıysa kırmızı yapıldı
        t.tag_configure('liste_disi', foreground='white', background='#e74c3c')
        
        # tabloyu çerçeveye tam oturacak şekilde yerleştirdik
        t.pack(fill="both", expand=True)
     
        # "<Double-1>": Farenin sol tuşuyla çift tıklama olayı sayesinde 
        # Herhangi bir öğrenciye çift tıklandığında detay pop-up ekranı açıldı
        t.bind("<Double-1>", lambda e: self.ogrenci_detay_popup(t))
        return t

    def ogrenci_detay_popup(self, tree):
        # tabloda bir öğrenciye çift tıklandığında tercihlerini gösteren küçük detay penceresini açar 
        
        # tablodaki seçili olan satırın ID alır
        secili = tree.selection()
        if not secili: return
        
        # seçili satırın içindeki veriler (ID, GNO, Firma, Sıra) bir sözlük olarak döndürüldü
        item_verisi = tree.item(secili[0])['values']
        ogr_id = str(item_verisi[0])     
        yerlesen_firma = item_verisi[2] 
        
        # tıklanan tablonun hangi algoritmaya ait olduğunu tespit edildi
        # bu sayede doğru veri listesinden arama yapıldı
        yontem = "Greedy" if tree == self.tree_g else "Heuristic"
        
        # listemizdeki binlerce öğrenci arasından ID'si eşleşen öğrenci objesini bulur
        ogrenci = next((o for o in self.sonuclar[yontem]['liste'] if str(o['id']) == ogr_id), None)
        
        if ogrenci:
            # tk.Toplevel ile ana pencerenin üzerinde açılan yeni bir bağımsız pencere oluşturuldu
            pencere = tk.Toplevel(self.root)
            pencere.title(f"Tercih Listesi - {ogr_id}")
            pencere.geometry("350x450") 
            pencere.configure(bg="#2c3e50") 
            
            # pencerenin üst kısmına öğrenci bilgileri (ID ve GNO) yazdırıldı
            tk.Label(pencere, text=f"Öğrenci: {ogr_id}", font=("Arial", 12, "bold"), fg="white", bg="#2c3e50").pack(pady=10)
            tk.Label(pencere, text=f"GNO: {ogrenci['gno']}", fg="#bdc3c7", bg="#2c3e50").pack()
            
            # tercihlerin listeleneceği alan oluşturuldu
            liste_alani = tk.Frame(pencere, bg="#34495e", padx=10, pady=10)
            liste_alani.pack(fill="both", expand=True, padx=20, pady=20)
            
            # öğrencinin yaptığı tercihler döngüye alarak alt alta yazdırıldı
            for i, t in enumerate(ogrenci['tercihler'], 1):
                # eğer döngüdeki firma öğrencinin yerleştiği firmaysa (aktifmi = True)
                aktifmi = (t == yerlesen_firma)
                
                # yerleştiği firma yeşil ve kalın fontla gösterildi diğerleri beyaz yapıldı
                renk = "#2ecc71" if aktifmi else "white"
                font = ("Arial", 10, "bold") if aktifmi else ("Arial", 10)
                # yerleştiği firmanın başına "***" işareti koyuldu ve  diğerlerine sıra numarası koyuldu
                simge = "*** " if aktifmi else f"{i}. "
                
                tk.Label(liste_alani, text=f"{simge}{t}", font=font, fg=renk, bg="#34495e", anchor="w").pack(fill="x", pady=2)
            
            # pencereyi kapatmaya yarayan kırmızı buton
            tk.Button(pencere, text="KAPAT", command=pencere.destroy, bg="#e74c3c", fg="white").pack(pady=10)

    def hesapla(self):
        #'Simülasyonu Başlat' butonuna basıldığında tüm hesaplama sürecini yöneten fonksiyon 
        
        # ilk olarak CSV dosyasındaki güncel verileri yüklemeyi dener.
        # eğer dosya bulunamazsa veya hata verirse 'veriyi_yukle' False döner ve işlem burada durur.
        if not self.sim.veriyi_yukle(): 
            return
        
        # StajSimulasyonu sınıfındaki 'calistir' metoduna 'Greedy' parametresini gönderir
        # ve dönen sonuçları sözlüğe kaydeder.
        self.sonuclar['Greedy'] = self.sim.calistir("Greedy")
        
        # aynı işlemi 'Heuristic' algoritma için de yapar.
        self.sonuclar['Heuristic'] = self.sim.calistir("Heuristic")
        
        self.tablolari_doldur()
        
        # alt bilgi çubuğundaki metin güncellendi ve rengi yeşile çevrildi
        self.lbl_info.config(text=" Hesaplandı. Detay için öğrenciye çift tıklayın.", fg="#27ae60")
        
        # hesaplama bittiği için daha önce tıklanamayan (disabled) 'Final Raporu' 
        # ve 'Adım Adım Analiz' butonlarını tıklanabilir (normal) hale getirir.
        self.btn_report.config(state="normal")
        self.btn_step.config(state="normal")

    def adim_adim_ekranı(self):
        #simülasyonun her turunu bir izlememizi sağlayan log ekranını kurulumu
        
        # ekranı temizleyip yepyeni bir analiz sayfası açtık
        for widget in self.main_container.winfo_children(): 
            widget.destroy()
        
        nav_bar = tk.Frame(self.main_container, bg="#2c3e50", pady=10)
        nav_bar.pack(fill="x")
        tk.Button(nav_bar, text="ANA SAYFAYA DÖN", command=self.ana_paneli_olustur, 
                  bg="#95a5a6", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=15)
        
        # kontrol butonunun (Sonraki Adım) duracağı alan
        control_frame = tk.Frame(self.main_container, pady=10)
        control_frame.pack(fill="x")
        
        # ana verileri bozmamak için kopyalarını alındı
        # 'ogr': Öğrenciler, 'kon': Kontenjanlar, 'tur': Kaçıncı turdayız, 'islem': Toplam deneme sayısı
        data_g = {"ogr": [o.copy() for o in self.sim.ogrenciler_master], "kon": self.sim.firmalar_master.copy(), "tur": 0, "islem": 0}
        data_h = {"ogr": [o.copy() for o in self.sim.ogrenciler_master], "kon": self.sim.firmalar_master.copy(), "tur": 0, "islem": 0}
        
        main_frame = tk.Frame(self.main_container)
        main_frame.pack(fill="both", expand=True, padx=10)

        def create_log_area(parent, title):
            # Algoritma çıktılarını yazdıracağımız siyah/beyaz konsol benzeri Text kutularını oluşturur 
            f = tk.LabelFrame(parent, text=title, font=("Arial", 11, "bold"))
            f.pack(side="left", fill="both", expand=True, padx=5)
            t = tk.Text(f, font=("Consolas", 10), bg="#f8f9fa") # Yazılımcı tipi font: Consolas
            t.pack(fill="both", expand=True, padx=5, pady=5)
            
            # yazıları renklendirmek için tag tanımları 
            t.tag_config("header", foreground="#2980b9", font=("Consolas", 10, "bold"))
            t.tag_config("green", foreground="#27ae60", font=("Consolas", 10, "bold"))
            t.tag_config("red", foreground="#e74c3c")
            t.tag_config("blue", foreground="#3498db", font=("Consolas", 10, "bold"))
            return t

        txt_g = create_log_area(main_frame, "GREEDY ALGORİTMASI")
        txt_h = create_log_area(main_frame, "HEURISTIC ALGORİTMASI")

        def iterasyon_islet(d, txt, yontem):
            #'Sonraki Adım'a basıldığında atama ve reddetme mantığını yürüten çekirdek fonksiyon 
            d["tur"] += 1
            yerlesmemisler = [o for o in d["ogr"] if o['durum'] == 'Yerlesmedi']
            
            if not yerlesmemisler:
                txt.insert(tk.END, f"\n--- {yontem} TAMAMLANDI ---\n", "green")
                return False # yerleşmemiş yoksa İşlem bitti
            
            txt.insert(tk.END, f"\n{'='*40}\n", "header")
            txt.insert(tk.END, f"TUR {d['tur']} BAŞLADI\n", "header")
            
            # sıralama farkı
            if yontem == "Greedy": 
                # sadece GNO'su yüksek olana öncelik verir
                yerlesmemisler.sort(key=lambda x: x['gno'], reverse=True)
            else: 
                # GNO'yu rastgele bir katsayıyla çarpar 
                yerlesmemisler.sort(key=lambda x: x['gno'] * (0.85 + random.random() * 0.3), reverse=True)
            
            for o in yerlesmemisler:
                d["islem"] += 1 
                atanabildi = False
                for idx, t in enumerate(o['tercihler']):
                    if d["kon"].get(t, 0) > 0: # eğer şirkette boş yer varsa
                        o['yerlestigi_firma'] = t
                        o['durum'] = 'Onerildi' # şirkete teklif edildi (Henüz kesinleşmedi)
                        d["kon"][t] -= 1
                        o['tercih_no'] = idx + 1
                        atanabildi = True
                        break
                
                # tercihleri doluysa boşta kalan bir şirkete rastgele ata
                if not atanabildi:
                    boslar = [f for f, k in d["kon"].items() if k > 0]
                    if boslar:
                        s = random.choice(boslar)
                        o['yerlestigi_firma'] = s
                        o['durum'] = 'Onerildi'
                        d["kon"][s] -= 1
                        o['tercih_no'] = "Rastgele"
            
            # şirket kabul ret süreci
            yeni_yerlesen_sayisi = 0
            reddedilenler = []
            for o in d["ogr"]:
                if o['durum'] == 'Onerildi':
                    # RED_ORANI (%20) ihtimalle şirket öğrenciyi reddeder
                    if random.random() < RED_ORANI:
                        firma = o['yerlestigi_firma']
                        reddedilenler.append(f"ID:{o['id']} | Firma:{firma}")
                        d["kon"][firma] += 1 # kontenjanı geri açtık
                        o['yerlestigi_firma'] = None
                        o['durum'] = 'Yerlesmedi'
                    else: 
                        o['durum'] = 'Yerlestirildi' # kesin kayıt yapıldı
                        yeni_yerlesen_sayisi += 1
            
            # analiz ekranına sonuçları yazdır
            txt.insert(tk.END, f" Bu turda yerleşen: {yeni_yerlesen_sayisi}\n", "green")
            if reddedilenler:
                txt.insert(tk.END, f" Reddedilenler ({len(reddedilenler)}):\n", "red")
                for r in reddedilenler: txt.insert(tk.END, f"   > {r}\n", "red")
            
            txt.insert(tk.END, f" Kalan Kontenjan: {sum(d['kon'].values())}\n", "blue")
            txt.see(tk.END) # otomatik olarak en alt satıra kaydır

            # Ana ekrana döndüğümüzde verilerin kaybolmaması için sonuçları self.sonuclar'a aktarır
            self.sonuclar[yontem] = {
                'liste': [o.copy() for o in d["ogr"]],
                'tur': d["tur"],
                'islem': d["islem"],
                'sure': 0.001
            }
            return True
        def ikisini_de_ilerlet():
            g = iterasyon_islet(data_g, txt_g, "Greedy")
            h = iterasyon_islet(data_h, txt_h, "Heuristic")
            if not g and not h: btn_next.config(state="disabled", text="Süreç Bitti")

        btn_next = tk.Button(control_frame, text="SONRAKİ ADIM ", command=ikisini_de_ilerlet, 
                            bg="#16a085", fg="white", font=("Arial", 11, "bold"), padx=20); btn_next.pack()

   

    def giris_kontrol(self):
        # şifre doğru mu kontrolü yapan yer 
        if self.ent_user.get() == GIRIS_BILGILERI["kullanici"] and self.ent_pass.get() == GIRIS_BILGILERI["sifre"]: 
            self.ana_paneli_olustur()
        else: 
            messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre!")

    def guvenli_cikis(self):
        # çıkarken bir soralım ki yanlışlıkla gitmesin her şey mantığı ile yapıldı
        if messagebox.askyesno("Çıkış", "Sistemden çıkış yapmak istediğinize emin misiniz?"): 
            self.giris_ekranini_olustur()

    def tablolari_doldur(self, filtre=""):    
        # döngü kurarak hem Greedy hem de Heuristic tablolarını tek tek işliyoruz
        for t, k in [(self.tree_g, 'Greedy'), (self.tree_h, 'Heuristic')]:

            t.delete(*t.get_children())
            
            # eğer o algoritmaya ait hesaplanmış bir sonuç varsa içeri giriyoruz
            if k in self.sonuclar:
                # o algoritmadaki tüm öğrencileri tek tek döngüye alıyoruz
                for o in self.sonuclar[k]['liste']:

                    if filtre in str(o['id']).lower():

                        firma = o['yerlestigi_firma'] if o['yerlestigi_firma'] else "Açıkta"
                        
                        # yerleştiği tercihin kaçıncı sırada olduğunu aldık
                        sira = o.get('tercih_no', '-') if o['yerlestigi_firma'] else "-"
                        
                        # yukarıdaki kodlar da da hep belirlendiği gibi
                        # sira == 1 ise: 'birinci' etiketi (Yeşil)
                        # sira == "Rastgele" ise: 'liste_disi' etiketi (Kırmızı)
                        # diğer tüm yerleşme durumları: 'diger_tercih' etiketi (Mavi)
                        tag = 'birinci' if sira == 1 else ('liste_disi' if sira == "Rastgele" else 'diger_tercih')
                        
                        # hazırladığımız tüm bu bilgileri tablonun en sonuna yeni bir satır olarak ekliyoruz
                        t.insert("", "end", values=(o['id'], o['gno'], firma, sira), tags=(tag,))

    def tabloyu_filtrele(self, *args): 
        self.tablolari_doldur(self.search_var.get().lower())

    def final_raporu_ekranı(self):
        for widget in self.main_container.winfo_children(): widget.destroy()
        
        # sayfanın üst tarafının ayarlanması
        nav_bar = tk.Frame(self.main_container, bg="#2c3e50", pady=10); nav_bar.pack(fill="x")
        tk.Button(nav_bar, text=" ANA SAYFAYA DÖN", command=self.ana_paneli_olustur, bg="#95a5a6", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=15)
        
        # performans tablosu oluşturuldu
        tk.Label(self.main_container, text=" PERFORMANS ÖZETİ", font=("Arial", 12, "bold"), bg="#ecf0f1").pack(pady=10)
        cols = ("Yöntem", "Toplam Tur", "Deneme", "Süre", "Memnuniyet Skoru")
        table = ttk.Treeview(self.main_container, columns=cols, show="headings", height=3)
        for c in cols: table.heading(c, text=c)
        table.pack(fill="x", padx=20)
        
        # her algoritma için özet veriyi hesapla ve ekle
        for k in ["Greedy", "Heuristic"]:
            s = self.sonuclar[k]
            mem = sum((5 - o['tercihler'].index(o['yerlestigi_firma'])) if (o['yerlestigi_firma'] and o['yerlestigi_firma'] in o['tercihler']) else 0 for o in s['liste'] if o['yerlestigi_firma'])
            table.insert("", "end", values=(k, s['tur'], s['islem'], f"{s['sure']:.4f}", mem))
        
        # detaylı şirket listeleri için sekmeli alan
        nb = ttk.Notebook(self.main_container); nb.pack(fill="both", expand=True, padx=20, pady=20)
        for y in ["Greedy", "Heuristic"]:
            f_frame = tk.Frame(nb); nb.add(f_frame, text=f"{y} Yerleşim Detayları")
            stxt = tk.Text(f_frame, font=("Consolas", 10)); stxt.pack(fill="both", expand=True)
            
            # hangi şirkete kimler gitti listesi oluşturuldu
            firmalar = {f: [] for f in self.sim.firmalar_master.keys()}
            for o in self.sonuclar[y]['liste']:
                if o['yerlestigi_firma']: firmalar[o['yerlestigi_firma']].append(f"{o['id']} (GNO: {o['gno']})")
            
            res = ""
            for f, ogs in firmalar.items():
                res += f" ŞİRKET: {f}\n" + ("   • " + "\n   • ".join(ogs) if ogs else "   (Boş)") + "\n\n"
            stxt.insert("1.0", res)

# programın başlatıldığı kısım
if __name__ == "__main__":
    root = tk.Tk()
    app = UygulamaGUI(root)
    root.mainloop()