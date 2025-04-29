import pyautogui
import pytesseract
from PIL import Image
import time
import os

# Optional: Pfad zu tesseract.exe setzen, falls Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_chat_screenshot(region=None):
    pyautogui.click(1850, 900)
    pyautogui.sleep(0.5)
    screenshot = pyautogui.screenshot(region=region)  # z.B. nur das Chat-Fenster
    return screenshot

def extract_text(image):
    configuration = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(image,lang='eng',config=configuration)  # oder 'chi_sim' für Chinesisch
    return text

def monitor_dingtalk(region=None, interval=5):
    print("Monitoring gestartet...")
    #while True:

    time.sleep(interval)
    
    screenshot = get_chat_screenshot(region)
    text = extract_text(screenshot)

    print(text)

    return text
    
        
        # for keyword in keywords:
        #     if keyword.lower() in text.lower():
        #         print(f"🎯 Schlüsselwort erkannt: {keyword} → Skript wird getriggert!")
        #         run_my_script()
        
        

def run_my_script():
    # Hier kannst du dein eigenes Python-Skript aufrufen oder Aktionen starten
    os.system("python mein_script.py")

if __name__ == "__main__":
    monitor_dingtalk(region = (400, 80, 500, 900))  # region anpassen!
