import pyautogui
import time
import os
import keras_ocr
import numpy as np
from PIL import Image

# Screenshot-Region (angepasst!)
region = (400, 80, 1075, 900)

# OCR-Pipeline initialisieren
pipeline = keras_ocr.pipeline.Pipeline()

def get_chat_screenshot(filename='screenshot.png'):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(filename)
    return filename

def extract_text_with_kerasocr(image_path):
    # Bild laden
    img = keras_ocr.tools.read(image_path)
    # Text erkennen
    prediction_groups = pipeline.recognize([img])
    predictions = prediction_groups[0]

    # Alle erkannten Wörter zusammenfassen
    text = " ".join([text for text, box in predictions])

    for word in predictions:
        #text = " ".join([text for text, box in predictions])
        print(f"Erkanntes Wort: {word[0]}")

    return text.strip()

def monitor_for_keywords(keywords, interval=5):
    print("📡 Monitoring gestartet...")
    # while True:
    time.sleep(interval)

    image_path = get_chat_screenshot()
    text = extract_text_with_kerasocr(image_path)
    print("🔍 Gelesener Text:", text)

    for keyword in keywords:
        if keyword.lower() in text.lower():
            print(f"🎯 Schlüsselwort erkannt: {keyword} → Skript wird getriggert!")
            run_my_script()

def run_my_script():
    # Beispiel: eigenes Skript starten
    os.system("python mein_script.py")

if __name__ == "__main__":
    monitor_for_keywords(["ALARM", "WICHTIG"], interval=5)
