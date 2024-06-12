import cv2
import dlib
import face_recognition
from datetime import datetime, timedelta
import time
import pypyodbc

# Veritabanı bağlantı bilgileri
connection_string = (
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=yuztanimaproje.database.windows.net;'
    'Database=yuztanima;'
    'UID=yusuf;'  
    'PWD=P@ssw0rd!;'
)

# Veritabanına bağlanma
try:
    connection = pypyodbc.connect(connection_string)
    print("Veritabanı bağlantısı başarılı!")
except pypyodbc.DatabaseError as e:
    print("Veritabanı bağlantısı başarısız:", e)
    exit(1)

# Cursor oluşturma
cursor = connection.cursor()

# SQL sorgusu (tabloya veri ekleme)
insert_query = """
INSERT INTO YOKLAMA (Ogrenci_No, Tarih)
VALUES (?, ?)
"""

# Veritabanına veriler yüklenirken kullanılacak metod
def ekle(numara, son_giris_zamani, simdiki_zaman):
    # Son giriş zamanını ve şimdiki zamanı datetime nesnesine çevirme
    zaman_simdiki = datetime.strptime(simdiki_zaman, "%H:%M")
    zaman_onceki = datetime.strptime(son_giris_zamani, "%H:%M")

    # Son girişten geçen saniye farkının hesaplanması
    fark = zaman_simdiki - zaman_onceki
    fark_saniye = fark.total_seconds()

    if fark_saniye > (40 * 60):  # 40 dakikadan fazla geçmişse
        try:
            cursor.execute(insert_query, (numara, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            connection.commit()
            print("Veri başarıyla eklendi!")
        except pypyodbc.DatabaseError as e:
            print("Veri eklenirken hata oluştu:", e)
        print(f"{numara} kaydedildi")
        return simdiki_zaman
    else:
        return son_giris_zamani

# Kişilerin yüz tanımları
temur = face_recognition.load_image_file("temur.jpg")
temur_enc = face_recognition.face_encodings(temur)[0]
temur_son_giris = "00:00"

baran = face_recognition.load_image_file("baran.jpg")
baran_enc = face_recognition.face_encodings(baran)[0]
baran_son_giris = "00:00"

emir = face_recognition.load_image_file("emir.jpg")
emir_enc = face_recognition.face_encodings(emir)[0]
emir_son_giris = "00:00"

ishak = face_recognition.load_image_file("ishak.jpg")
ishak_enc = face_recognition.face_encodings(ishak)[0]
ishak_son_giris = "00:00"

yusuf = face_recognition.load_image_file("yusuf.jpg")
yusuf_enc = face_recognition.face_encodings(yusuf)[0]
yusuf_son_giris = "00:00"

kurt = face_recognition.load_image_file("kurt.jpg")
kurt_enc = face_recognition.face_encodings(kurt)[0]
kurt_son_giris = "00:00"

# Yüz dedektörü
detector = dlib.get_frontal_face_detector()

# Kameradan görüntü alma
cap = cv2.VideoCapture(0)

try:
    while True:
        time.sleep(0.3)
        ret, frame = cap.read()
        face_loc = []
        faces = detector(frame)

        for face in faces:
            x = face.left()
            y = face.top()
            w = face.right()
            h = face.bottom()
            face_loc.append((y, w, h, x))

        face_enc = face_recognition.face_encodings(frame, face_loc)

        for i, face in enumerate(face_enc):
            y, w, h, x = face_loc[i]

            temur_s = face_recognition.compare_faces([temur_enc], face)
            kurt_s = face_recognition.compare_faces([kurt_enc], face)
            baran_s = face_recognition.compare_faces([baran_enc], face)
            emir_s = face_recognition.compare_faces([emir_enc], face)
            ishak_s = face_recognition.compare_faces([ishak_enc], face)
            yusuf_s = face_recognition.compare_faces([yusuf_enc], face)


            current_time = datetime.now().strftime('%H:%M')
            if temur_s[0]:
                cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 3)
                cv2.putText(frame, "221821 Mustafa Temur TUARAN", (x, h + 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                temur_son_giris = ekle("221821", temur_son_giris, current_time)
            elif kurt_s[0]:
                cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 3)
                cv2.putText(frame, "1002 Mustafa KURT", (x, h + 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                kurt_son_giris = ekle("1002", kurt_son_giris, current_time)
            elif baran_s[0]:
                cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 3)
                cv2.putText(frame, "221872 Baran ASAR", (x, h + 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                baran_son_giris = ekle("221872", baran_son_giris, current_time)
            elif emir_s[0]:
                cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 3)
                cv2.putText(frame, "221849 Emir COSKUN", (x, h + 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                emir_son_giris = ekle("221849", emir_son_giris, current_time)
            elif ishak_s[0]:
                cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 3)
                cv2.putText(frame, "231833 Ishak YORGACI", (x, h + 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                ishak_son_giris = ekle("231833", ishak_son_giris, current_time)
            elif yusuf_s[0]:
                cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 3)
                cv2.putText(frame, "221856 Yusuf DUMAN", (x, h + 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
                yusuf_son_giris = ekle("221856", yusuf_son_giris, current_time)
            else:
                cv2.rectangle(frame, (x, y), (w, h), (255, 0, 0), 3)
                cv2.putText(frame, "Yabancı", (x, h + 35), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        cv2.imshow("deneme", frame)
        if cv2.waitKey(10) & 0xFF == ord("q"):
            break
finally:
    # Kaynakları serbest bırak
    cap.release()
    cv2.destroyAllWindows()
    connection.close()
