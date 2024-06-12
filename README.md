# Yüz Tanıma ve Yoklama Sistemi

Bu proje, yüz tanıma kullanarak yoklama alma işlemi gerçekleştiren bir sistemdir. OpenCV, dlib ve face_recognition kütüphanelerini kullanarak canlı kamera görüntüsünden yüzleri tanır ve sql veritabanına yoklama bilgilerini kaydeder.

## Gereksinimler

- Python 
- OpenCV
- dlib
- face_recognition
- pypyodbc

## Kurulum

1. Gerekli Python kütüphanelerini yükleyin:
    ```sh
    pip install opencv-python
    pip install dlib
    pip install face_recognition
    pip install pypyodbc
    ```

2. Veritabanı bağlantı bilgilerinizi güncelleyin(bu kısma kullanacağınız sql veri tabanının bilgilerini yazmanız gerekmektedir):
    ```python
    connection_string = (
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=yuztanimaproje.database.windows.net;'
        'Database=yuztanima;'
        'UID=yusuf;'  
        'PWD=P@ssw0rd!;'
    )
    ```

3. Tanıyacağınız kişilerin yüz resimlerini proje dizinine ekleyin ve kodda uygun yerlere dosya adlarını girin:
    ```python
    temur = face_recognition.load_image_file("temur.jpg")
    temur_enc = face_recognition.face_encodings(temur)[0]
    ```

## Kullanım

1. Projeyi çalıştırın:
    ```sh
    python yuz_tanima.py
    ```

2. Kamera açılacak ve yüz tanıma işlemi başlayacaktır. Tanınan yüzler veritabanına kaydedilecektir.

3. Çıkmak için `q` tuşuna basın.

## Yöntemler

### ekle(numara, son_giris_zamani, simdiki_zaman)
Bu yöntem, öğrenci numarası ve giriş zamanını alarak veritabanına yoklama bilgisi olarak ekler.

## Lisans

Bu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için `LICENSE` dosyasına bakın.
