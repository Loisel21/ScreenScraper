import pyautogui
import pytesseract
from PIL import Image
import time
import os
from datetime import datetime
import re

# Optional: Pfad zu tesseract.exe setzen, falls Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Screenshot-Region (angepasst!)
region = (400, 80, 500, 900) # Region anpassen!
interval = 1  # Zeitintervall in Sekunden

min_1 = ['1min', '1 min', '1minute', '1 minutes']
min_3 = ['3min', '3 min', '3minutes', '3 minutes']
min_5 = ['5min', '5 min', '5minutes', '5 minutes']

game_disc = ['disc', 'discs']
game_block = ['block', 'blocks']
game_redgreen = ['red green', 'red_green', 'redgreen']

current_game = None
current_state = None
current_no = None
current_stage = None
current_instruction = None

game_red = ['red']
game_green = ['green', 'gn', 'grn', 'gm', 'gr']
game_state_odd = ['odd', '0dd']
game_state_even = ['even', 'evn']

losing_states = ['lose', 'loss', 'los', 'lost']
winning_states = ['win', 'winn', 'winner', 'won', 'wn']

def build_pattern(words):
    return '|'.join(re.escape(word) for word in words)

# Gruppen zusammenfassen
state_pattern_odd_even = build_pattern(game_state_odd + game_state_even)
state_pattern_red_green = build_pattern(game_red + game_green)
result_pattern = build_pattern(losing_states + winning_states)

# Zwei separate Regexe (case-insensitive)
regex_odd_even = re.compile(
    rf'\b(\d{{2,3}})\s+({state_pattern_odd_even})\s+(?:stage\s*)?(\d+)(?:\s+({result_pattern}))?\b',
    re.IGNORECASE
)

regex_red_green = re.compile(
    rf'\b(\d{{2,3}})\s+({state_pattern_red_green})\s+(?:stage\s*)?(\d+)(?:\s+({result_pattern}))?\b',
    re.IGNORECASE
)


allowed_times = [
    ((11, 0), (11, 59)),  # von 11:00 bis 11:59
    ((13, 0), (13, 59)),  # von 13:00 bis 13:59
    ((18, 0), (18, 59)),  # von 18:00 bis 18:59
    ((20, 0), (20, 59)),  # von 20:00 bis 20:59
]


def get_chat_screenshot(region=None):
    pyautogui.click(1850, 900)
    pyautogui.sleep(0.5)
    screenshot = pyautogui.screenshot(region=region)  # z.B. nur das Chat-Fenster
    return screenshot


def extract_text(image):
    configuration = r'--oem 3 --psm 6'

    text = pytesseract.image_to_string(image,lang='eng',config=configuration)  # oder 'chi_sim' für Chinesisch
    return text


def monitor_dingtalk(region=None):
    
    screenshot = get_chat_screenshot(region)
    text = extract_text(screenshot)
    
    return text

        
        # for keyword in keywords:
        #     if keyword.lower() in text.lower():
        #         print(f"🎯 Schlüsselwort erkannt: {keyword} → Skript wird getriggert!")
        #         run_my_script()
        
        

def run_my_script():
    # Hier kannst du dein eigenes Python-Skript aufrufen oder Aktionen starten
    os.system("python mein_script.py")

def is_within_allowed_time():
    now = datetime.now()
    for start, end in allowed_times:
        start_hour, start_minute = start
        end_hour, end_minute = end

        if (now.hour > start_hour or (now.hour == start_hour and now.minute >= start_minute)) and \
           (now.hour < end_hour or (now.hour == end_hour and now.minute <= end_minute)):
            return True
    return False


def get_game(message):
    for game in games:
        if game.lower() in message.lower():
            return game
        
    return None

def get_game_values(current_game, message):
    if current_game in game_disc:
        pattern = regex_odd_even
    elif current_game in game_block:
        pattern = regex_odd_even
    elif current_game in game_redgreen:
        pattern = regex_red_green
    else:
        print("Unbekanntes Spiel")
        return None, None, None, None

    matches = re.findall(pattern, message)
    if matches:
        last_match = matches[-1]
        if current_no != last_match[1]:
            current_no = last_match[1]
            current_instruction = last_match[2]
            current_stage = last_match[3]
            current_state = last_match[4]
            return current_no, current_instruction, current_stage, current_state
        else:
            return None, None, None, None


def process_message(message):
    message = message.lower()

    if current_game is None:
        current_game = get_game(message)

    if current_game != None:
        game_values = get_game_values(current_game, message)
        if game_values:
            current_no, current_instruction, current_stage, current_state = game_values
            print(f"Spiel: {current_game}, No: {current_no}, Instruction: {current_instruction}, Stage: {current_stage}, State: {current_state}")


    # for keyword in prefix_words:
    #     if keyword.lower() in message.lower():
    #         print(f"🎯 Schlüsselwort erkannt: {keyword} → Skript wird getriggert!")

    

if __name__ == "__main__":
    print("Monitoring gestartet...")

    while True:
        if is_within_allowed_time():
            message = monitor_dingtalk(region = region)
            process_message(message)
        else:
            current_game = None
            current_state = None
            current_no = None
            current_stage = None
            current_instruction = None

        time.sleep(interval)
