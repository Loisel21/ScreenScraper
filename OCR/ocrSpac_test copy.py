import pyautogui
import time
import os
import requests
import json
from PIL import Image

# 🔑 Dein OCR.Space API Key hier eintragen!
API_KEY = 'K87579398588957'  # <-- Ersetzen mit deinem echten Key

# Screenshot-Region (angepasst an roten Rahmen im letzten Screenshot)
region = (400, 80, 1075, 900)

def get_chat_screenshot(filename='screenshot.png'):
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(filename)
    return filename

def ocr_space_file(filename, overlay=False, api_key=API_KEY, language='eng'):
    payload = {
        'isOverlayRequired': overlay,
        'apikey': api_key,
        'language': language,
        'isTable': True
    }
    with open(filename, 'rb') as f:
        r = requests.post(
            'https://api.ocr.space/parse/image',
            files={filename: f},
            data=payload,
        )
    return r.content.decode()

def extract_text_with_ocrspace(image_path):
    response = ocr_space_file(filename=image_path, api_key=API_KEY, language='eng')
    result_json = json.loads(response)
    try:
        return result_json["ParsedResults"][0]["ParsedText"].strip()
    except (KeyError, IndexError):
        return ""

def monitor_for_keywords(keywords, interval=5):
    print("📡 Monitoring gestartet...")
    # while True:
    time.sleep(interval)

    image_path = get_chat_screenshot()
    text = extract_text_with_ocrspace(image_path)
    print("🔍 Gelesener Text:", text)

    # for keyword in keywords:
    #     if keyword.lower() in text.lower():
    #         print(f"🎯 Schlüsselwort erkannt: {keyword} → Skript wird getriggert!")
    #         run_my_script()

def run_my_script():
    # Beispiel: eigenes Skript starten
    os.system("python mein_script.py")

if __name__ == "__main__":
    monitor_for_keywords(["ALARM", "WICHTIG"], interval=5)
