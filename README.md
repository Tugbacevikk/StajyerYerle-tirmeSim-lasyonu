# 🎓 Staj Atama Sistemi  (Greedy vs Heuristic Simülasyonu)

Bu proje, üniversitelerdeki staj yerleştirme sürecini **simülasyon ortamında** incelemek için geliştirilmiş bir Python uygulamasıdır. Sistem, öğrencilerin **GNO (Genel Not Ortalaması)** ve **firma tercihleri** üzerinden iki farklı algoritma kullanarak yerleştirme yapar:

* **Greedy Algoritması** → Başarı (GNO) öncelikli, kesin sıralama
* **Heuristic Algoritması** → Başarı + firma popülerliği + rastgelelik içeren esnek yaklaşım

Uygulama, akademisyenler için tasarlanmış bir **grafik arayüz (Tkinter GUI)** içerir ve sonuçları hem tablo hem de adım adım analiz ekranında karşılaştırmalı olarak sunar.

---

## 🚀 Özellikler

* 🔐 **Akademisyen Giriş Paneli**
* 📊 **Greedy ve Heuristic karşılaştırmalı sonuç ekranı**
* 🔍 Öğrenci ID ile **canlı arama ve filtreleme**
* 🖱️ Öğrenciye çift tıklayarak **tercih detaylarını görüntüleme**
* 🧪 **Adım Adım Simülasyon Modu** (her turu canlı izleme)
* 📝 **Final Raporu**

  * Toplam tur sayısı
  * Deneme sayısı
  * Çalışma süresi
  * Memnuniyet skoru
* 🧾 **Otomatik CSV veri üretici**
* ❌ Firma reddi simülasyonu (%20 olasılık)

---

## 🗂️ Proje Dosya Yapısı

```
📁 proje_klasoru
│
├── gui_app.py               # Ana uygulama (GUI + simülasyon kontrolü)
├── greedy.py              # Greedy atama algoritması
├── heuristic.py          # Heuristic atama algoritması
├── hazırStajVerileri.csv# Örnek / hazır veri seti
├── veri_uret.py         # Rastgele veri üretici modül
├── veri_uret_calistir.py# Veri üretici çalıştırıcı
└── README.md            # Proje dokümantasyonu
```

---

## 🧠 Algoritmaların Mantığı

###  Greedy Algoritması

**Yaklaşım:**

* Öğrenciler GNO’ya göre **yüksekten düşüğe sıralanır**
* Her öğrenci, tercih listesindeki ilk uygun firmaya atanır
* Kontenjan doluysa sıradaki tercihe geçilir
* Hiçbir tercih uygun değilse, **rastgele boş firma atanır**
* Firma, %20 ihtimalle öğrenciyi reddedebilir

**Avantaj:**

* Hızlı ve deterministik
* Akademik başarıyı maksimum önceliklendirir

**Dezavantaj:**

* Popüler firmalarda yığılma olabilir

---

###  Heuristic Algoritması

**Yaklaşım:**
Her öğrenci için özel bir skor hesaplanır:

```
Skor = (GNO × 2.0) + (Tercihlerin Ortalama Popülerliği × 0.05) + Rastgelelik
```

Bu sayede:

* Yüksek notlu öğrenciler korunur
* Aşırı popüler firmalarda tıkanma azaltılır
* Küçük rastgelelik sayesinde daha dengeli dağılım sağlanır

**Avantaj:**

* Daha adil ve dengeli yerleştirme
* Gerçek hayata daha yakın simülasyon

---

## 🖥️ Kurulum

### 1️ Gerekli Kütüphaneler

Python 3.9+ önerilir.

Terminal / CMD üzerinden:

```bash
pip install pandas numpy
```

Tkinter genellikle Python ile birlikte gelir.

---

## ▶️ Çalıştırma

### Ana Uygulama

```bash
python gui_app.py
```

### Varsayılan Giriş Bilgileri

```
Kullanıcı: akademisyen
Şifre: 1234
```

---

## 📄 Veri Formatı (CSV)

Sistem, aşağıdaki sütunları içeren `;` ayracıyla ayrılmış bir CSV dosyası kullanır:

| Firmalar | Kontenjanlar | Öğrenci | Tercih Sırası           | GNO  |
| -------- | ------------ | ------- | ----------------------- | ---- |
| Firma_1  | 3            | Ogr001  | Firma_3,Firma_1,Firma_5 | 3,45 |

> GNO değerleri Türkçe format için **virgüllü (3,45)** olarak yazılmalıdır.

---

## 🧪 Otomatik Veri Üretme

Yeni rastgele veri seti oluşturmak için:

```bash
python veri_uret_calistir.py
```

Bu komut:

* 120 öğrenci
* 50 firma
* Her öğrenci için 5 tercih

içeren `uretilenStajVerileri.csv` dosyasını üretir.

---

## 📊 Final Raporu İçeriği

* Toplam tur sayısı
* Toplam deneme sayısı
* Algoritma çalışma süresi
* **Memnuniyet Skoru**

### Memnuniyet Hesabı

Öğrenci kaçıncı tercihine yerleştiyse o kadar yüksek puan alır:

| Tercih    | Skor   |
| --------- | ------ |
| 1. tercih | 5 puan |
| 2. tercih | 4 puan |
| 3. tercih | 3 puan |
| Rastgele  | 0 puan |

---

## 🎯 Eğitimsel Amaç

Bu proje özellikle şu alanlarda kullanılmak üzere tasarlanmıştır:

* Algoritma karşılaştırması (Greedy vs Heuristic)
* Simülasyon tabanlı sistem analizi
* Yazılım mühendisliği (GUI + backend entegrasyonu)
* Veri yapıları ve performans ölçümü

---

## 📌 Geliştirme Fikirleri

* 📈 Grafiksel istatistik ekranı (matplotlib)
* 🌐 Web tabanlı sürüm (Flask / FastAPI)
* 🏫 Çoklu bölüm / fakülte desteği
* 🧑‍💼 Firma tarafı için ayrı panel

---

## 👨‍💻 Geliştirici Notu

Bu sistem, akademik projeler ve simülasyon tabanlı algoritma analizleri için modüler yapıda geliştirilmiştir. Yeni algoritmalar kolayca `calistir()` fonksiyonuna eklenebilir.

---
## Geliştiriciler

Erva Nur Bostancı

Nurgül Sarıtaş

Tuğba Çevik

---

## 📜 Lisans

Bu proje eğitim ve akademik kullanım amaçlıdır. Serbestçe geliştirilebilir ve genişletilebilir.

---

