import cv2
import numpy as np

def get_limits(color):
    """
    BGR renk değerinden HSV alt ve üst sınırları hesaplar
    Args:
        color: BGR formatında renk listesi [B, G, R]
    Returns:
        tuple: (lowerLimit, upperLimit) HSV formatında
    """
    # BGR değerini numpy array'e çevir ve reshape et
    c = np.uint8([[color]])  # BGR values
    
    # BGR'den HSV'ye dönüştür
    hsvC = cv2.cvtColor(c, cv2.COLOR_BGR2HSV)
    
    # Hue değerini al
    hue = hsvC[0][0][0]  # Get the hue value
    
    print(f"BGR: {color} -> HSV: {hsvC[0][0]} -> Hue: {hue}")  # Debug için
    
    # Kırmızı renk için özel durum (hue wrap-around)
    if hue >= 165:  # Kırmızının üst sınırı
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([180, 255, 255], dtype=np.uint8)
    elif hue <= 15:  # Kırmızının alt sınırı
        lowerLimit = np.array([0, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    else:  # Diğer renkler için normal aralık
        lowerLimit = np.array([hue - 10, 100, 100], dtype=np.uint8)
        upperLimit = np.array([hue + 10, 255, 255], dtype=np.uint8)
    
    return lowerLimit, upperLimit

# Test fonksiyonu
def test_get_limits():
    """Farklı renklerle fonksiyonu test et"""
    test_colors = {
        'Kırmızı': [0, 0, 255],
        'Mavi': [255, 0, 0], 
        'Yeşil': [0, 255, 0],
        'Sarı': [0, 255, 255],
        'Mor': [255, 0, 255],
        'Turuncu': [0, 165, 255]
    }
    
    for color_name, bgr_color in test_colors.items():
        lower, upper = get_limits(bgr_color)
        print(f"{color_name}: Lower={lower}, Upper={upper}")

if __name__ == "__main__":
    test_get_limits()