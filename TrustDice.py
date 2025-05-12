from pywinauto.application import Application
from pywinauto.mouse import click
import pytesseract
from PIL import Image
import time
import os
from datetime import datetime
import re

use_Testmode = False
deactivate_click = False

last_no = None

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

allowed_times = [
    ((11, 0), (11, 59)),
    ((13, 0), (13, 59)),
    ((18, 0), (18, 59)),
    ((20, 0), (20, 59)),
]

def is_within_allowed_time():
    now = datetime.now()
    for start, end in allowed_times:
        if (now.hour > start[0] or (now.hour == start[0] and now.minute >= start[1])) and \
           (now.hour < end[0] or (now.hour == end[0] and now.minute <= end[1])):
            return True
    return False

def laufzeit_messen(func):
    def wrapper(*args, **kwargs):
        if is_within_allowed_time() or use_Testmode:
            start = time.time()
            result = func(*args, **kwargs)
            ende = time.time()
            #print(f"[{func.__name__}] Laufzeit: {ende - start:.4f} Sekunden")
            with open("game_log.txt", "a", encoding="utf-8") as logfile:
                logfile.write(f"[{func.__name__}] Laufzeit: {ende - start:.4f} Sekunden\n")
            return result
    return wrapper

region = (400, 80, 500, 900)
interval = 1
bet_steps = [0.1, 0.3, 0.9, 2.7, 8.1, 24.3, 72.9, 218.7]

min_1 = ['1min', '1 min', '1minute', '1 minutes']
min_3 = ['3min', '3 min', '3minutes', '3 minutes']
min_5 = ['5min', '5 min', '5minutes', '5 minutes']

game_discs = ['disc', 'discs']
game_blocks = ['block', 'blocks']
game_redgreen = ['red green', 'red_green', 'redgreen', 'red - green', 'red-green']

game_red = ['red']
game_green = ['green', 'gn', 'grn', 'gm', 'gr']
game_state_odd = ['odd', '0dd']
game_state_even = ['even', 'evn']

losing_states = ['lose', 'loss', 'los', 'lost']
winning_states = ['win', 'winn', 'winner', 'won', 'wn']

current_game = None
current_state = None
current_no = None
current_stage = None
current_instruction = None
current_minute = None

#@laufzeit_messen
def build_pattern(words):
    return '|'.join(re.escape(word) for word in words)

state_pattern_odd_even = build_pattern(game_state_odd + game_state_even)
state_pattern_red_green = build_pattern(game_red + game_green)
result_pattern = build_pattern(losing_states + winning_states)

min_1_pattern = build_pattern(min_1)
min_3_pattern = build_pattern(min_3)
min_5_pattern = build_pattern(min_5)

combined_pattern = rf'\b({min_1_pattern}|{min_3_pattern}|{min_5_pattern})\b'
compiled_regex = re.compile(combined_pattern, re.IGNORECASE)

regex_odd_even = re.compile(
    rf'\b(\d{{2,3}})\s+({state_pattern_odd_even})\s+(?:stage\s*)?(\d+)(?:\s+({result_pattern}))?\b',
    re.IGNORECASE
)

regex_red_green = re.compile(
    rf'\b(\d{{2,3}})\s+({state_pattern_red_green})\s+(?:stage\s*)?(\d+)(?:\s+({result_pattern}))?\b',
    re.IGNORECASE
)



#@laufzeit_messen
def get_chat_screenshot(region=None):
    try:
        if not hasattr(get_chat_screenshot, "cached_app"):
            get_chat_screenshot.cached_app = Application(backend="uia").connect(title_re=".*DingTalk.*")
        app = get_chat_screenshot.cached_app
        window = app.window(title_re=".*DingTalk.*")

        window.set_focus()

        if use_Testmode == False and deactivate_click == False:
            window.click_input(coords=(1850, 900))  # Simulierter Klick innerhalb des Fensters

        time.sleep(1)
        rect = window.rectangle()
        left, top = rect.left + region[0], rect.top + region[1]
        right, bottom = left + region[2], top + region[3]
        img = window.capture_as_image().crop((region[0], region[1], region[0]+region[2], region[1]+region[3]))
        return img
    except Exception as e:
        print(f"Screenshot-Fehler: {e}")
        return None

#@laufzeit_messen
def extract_text(image):
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, lang='eng', config=config)
    return text

def monitor_dingtalk(region=None):
    screenshot = get_chat_screenshot(region)
    if screenshot:
        return extract_text(screenshot)
    return ""



#@laufzeit_messen
def extract_minutes(text):
    for minute in min_1:
        if minute in text:
            return 1
    for minute in min_3:
        if minute in text:
            return 3
    for minute in min_5:
        if minute in text:
            return 5
    return None

#@laufzeit_messen
def detect_current_game(message):
    if re.search(rf'({build_pattern(game_discs)})', message): return 'discs'
    if re.search(rf'({build_pattern(game_blocks)})', message): return 'blocks'
    if re.search(rf'({build_pattern(game_redgreen)})', message): return 'redgreen'
    return None

#@laufzeit_messen
def get_game_values(current_game, message):
    global current_no, current_instruction, current_stage, current_state
    pattern = regex_odd_even if current_game in game_discs + game_blocks else regex_red_green
    matches = re.findall(pattern, message)
    if matches:
        last_match = matches[-1]
        current_no, current_instruction, current_stage, current_state = last_match
        current_instruction = normalize_instruction(current_instruction)
    return current_no, current_instruction, current_stage, current_state

#@laufzeit_messen
def normalize_instruction(text):
    # Reihenfolge beachten: zuerst green prüfen, da sie mehrere Synonyme hat
    for word in game_green:
        if word in text:
            return 'green'
    for word in game_red:
        if word in text:
            return 'red'
    for word in game_state_odd:
        if word in text:
            return 'odd'
    for word in game_state_even:
        if word in text:
            return 'even'

    return None  # wenn nichts gefunden wurde

#@laufzeit_messen
def process_message(message):
    global current_minute, current_game, current_no, current_instruction, current_stage, current_state, last_no
    message = message.lower()
    if current_minute is None:
        current_minute = extract_minutes(message)
    if current_game is None:
        current_game = detect_current_game(message)
    if current_game:
        values = get_game_values(current_game, message)
        if values and last_no != current_no:
            if current_state == '':
                last_no = current_no
                print(f"Spiel: {current_game}, No: {current_no}, Instruction: {current_instruction}, Stage: {current_stage}, State: {current_state}, Minute: {current_minute}")
                with open("game_log.txt", "a", encoding="utf-8") as logfile:
                    logfile.write(f"{datetime.now().isoformat()} | Spiel: {current_game}, Minute: {current_minute}, No: {current_no}, Instruction: {current_instruction}, Stage: {current_stage}, State: {current_state}\n")
                return True
    return False

                

if __name__ == "__main__":
    print("Monitoring gestartet...")
    while True:
        if is_within_allowed_time() or use_Testmode:
            start_time = datetime.now()

            message = monitor_dingtalk(region=region)
            processed = process_message(message)

            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()

            with open("game_log.txt", "a", encoding="utf-8") as logfile:
                logfile.write(f"{end_time.isoformat()} | Verarbeitung dauerte {duration:.2f} Sekunden.\n")

            if processed:
                last_processed_time = datetime.now()
            # else:
            #     if last_processed_time:
            #         elapsed = (datetime.now() - last_processed_time).total_seconds()
            #         if elapsed > 240:
            #             print(f"Achtung: Seit über 4 Minuten ({int(elapsed)}s) keine Verarbeitung erfolgt.")
            #             with open("game_log.txt", "a", encoding="utf-8") as logfile:
            #                 logfile.write(f"{datetime.now().isoformat()} | Achtung: Seit über 4 Minuten ({int(elapsed)}s) keine Verarbeitung erfolgt.\n")
            #     else:
            #         print("Noch keine Verarbeitung erfolgt.")
            #         with open("game_log.txt", "a", encoding="utf-8") as logfile:
            #             logfile.write(f"{datetime.now().isoformat()} | Noch keine Verarbeitung erfolgt.\n")
        else:
            current_game = current_state = current_no = current_stage = current_instruction = current_minute = last_no = last_stage = None
            last_processed_time = None
