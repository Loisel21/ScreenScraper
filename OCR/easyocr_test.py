import pyautogui
import easyocr
from PIL import Image
import time
import os

# Optional: Pfad zu tesseract.exe setzen, falls Windows
#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_chat_screenshot(region=None):
    screenshot = pyautogui.screenshot('myScreenshot.png',region=region)  # z.B. nur das Chat-Fenster
    return screenshot

def extract_text(image):
    # text = pytesseract.image_to_string(image, lang='eng')  # oder 'chi_sim' für Chinesisch
    #text = pytesseract.image_to_data(image, lang='eng')
    #results = easyocr.rea('myScreenshot.png')  # oder ['en', 'zh'] für Englisch+Chinesisch
    reader = easyocr.Reader(['en'], gpu=False)  # oder ['en', 'zh'] für Englisch + Chinesisch
    results = reader.readtext('myScreenshot.png', detail=0, paragraph=True)  # detail=0 gibt nur den Text zurück, ohne Bounding Box und Confidence

    # for bbox, text, confidence in results:
    #     print(f"Erkannt: {text} (Confidence: {confidence:.2f})")

    return results

def monitor_for_keywords(keywords, region=None, interval=5):
    print("Monitoring gestartet...")
    #while True:
    time.sleep(interval)


    screenshot = get_chat_screenshot(region)
    text = extract_text(screenshot)
    print("Gelesener Text:", text)
    
    # for keyword in keywords:
    #     if keyword.lower() in text.lower():
    #         print(f"🎯 Schlüsselwort erkannt: {keyword} → Skript wird getriggert!")
    #         run_my_script()
        
        

def run_my_script():
    # Hier kannst du dein eigenes Python-Skript aufrufen oder Aktionen starten
    # os.system("python mein_script.py")
    print("Mein Skript wird jetzt ausgeführt!")

if __name__ == "__main__":
    # Beispiel: Nur nach dem Wort "ALARM" oder "WICHTIG" suchen
    monitor_for_keywords(["3 minutes RED_GREEN", "WICHTIG"], region = (400, 80, 1075, 900))  # region anpassen!
