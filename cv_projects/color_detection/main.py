import cv2
import numpy as np
from utils import get_limits

# Tespit edilecek renk (BGR formatında)
yellow = [0, 255, 255]  # Sarı renk
# Diğer renk örnekleri:
# red = [0, 0, 255]     # Kırmızı
# blue = [255, 0, 0]    # Mavi  
# green = [0, 255, 0]   # Yeşil

cap = cv2.VideoCapture(0)

# Kamera açılıp açılmadığını kontrol et
if not cap.isOpened():
    print("Kamera açılamadı!")
    exit()

while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Kamera görüntüsü alınamadı!")
        break
    
    # BGR'den HSV'ye dönüştür
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Renk sınırlarını al
    lowerLimit, upperLimit = get_limits(color=yellow)
    
    # Maske oluştur
    mask = cv2.inRange(hsv_frame, lowerLimit, upperLimit)
    
    # Maskeyi orijinal görüntüye uygula
    result = cv2.bitwise_and(frame, frame, mask=mask)
    
    # Konturları bul (opsiyonel - tespit edilen alanları çerçevele)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Büyük konturları çerçevele
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Minimum alan
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Sari Tespit Edildi', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    # Görüntüleri göster
    cv2.imshow('Orijinal', frame)
    cv2.imshow('Maske', mask)
    cv2.imshow('Sonuc', result)
    
    # 'q' tuşuna basılırsa çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()