from pywinauto.application import Application
from pywinauto.mouse import click
import pytesseract
from PIL import Image
import time
import os
from datetime import datetime
import re

last_no = None

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

region = (400, 80, 500, 900)
interval = 1

min_1 = ['1min', '1 min', '1minute', '1 minutes']
min_3 = ['3min', '3 min', '3minutes', '3 minutes']
min_5 = ['5min', '5 min', '5minutes', '5 minutes']

game_disc = ['disc', 'discs']
game_block = ['block', 'blocks']
game_redgreen = ['red green', 'red_green', 'redgreen']

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

allowed_times = [
    ((11, 0), (11, 59)),
    ((13, 0), (13, 59)),
    ((18, 0), (18, 59)),
    ((20, 0), (20, 59)),
]

def get_chat_screenshot(region=None):
    try:
        app = Application(backend="uia").connect(title_re=".*DingTalk.*")
        window = app.window(title_re=".*DingTalk.*")
        window.set_focus()
        window.click_input(coords=(1850, 900))  # Simulierter Klick innerhalb des Fensters
        time.sleep(0.5)
        rect = window.rectangle()
        left, top = rect.left + region[0], rect.top + region[1]
        right, bottom = left + region[2], top + region[3]
        img = window.capture_as_image().crop((region[0], region[1], region[0]+region[2], region[1]+region[3]))
        return img
    except Exception as e:
        print(f"Screenshot-Fehler: {e}")
        return None

def extract_text(image):
    config = r'--oem 3 --psm 6'
    text = pytesseract.image_to_string(image, lang='eng', config=config)
    return text

def monitor_dingtalk(region=None):
    screenshot = get_chat_screenshot(region)
    if screenshot:
        return extract_text(screenshot)
    return ""

def is_within_allowed_time():
    now = datetime.now()
    for start, end in allowed_times:
        if (now.hour > start[0] or (now.hour == start[0] and now.minute >= start[1])) and \
           (now.hour < end[0] or (now.hour == end[0] and now.minute <= end[1])):
            return True
    return False

def extract_minutes(text):
    match = compiled_regex.search(text)
    if not match:
        return None
    value = match.group(1).lower()
    if value in map(str.lower, min_1): return 1
    elif value in map(str.lower, min_3): return 3
    elif value in map(str.lower, min_5): return 5
    return None

def detect_current_game(message):
    if re.search(rf'\b({build_pattern(game_disc)})\b', message): return 'disc'
    if re.search(rf'\b({build_pattern(game_block)})\b', message): return 'block'
    if re.search(rf'({build_pattern(game_redgreen)})', message): return 'redgreen'
    return None

def get_game_values(current_game, message):
    global current_no, current_instruction, current_stage, current_state
    pattern = regex_odd_even if current_game in game_disc + game_block else regex_red_green
    matches = re.findall(pattern, message)
    if matches:
        last_match = matches[-1]
        current_no, current_instruction, current_stage, current_state = last_match
    return current_no, current_instruction, current_stage, current_state

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
            last_no = current_no
            print(f"Spiel: {current_game}, No: {current_no}, Instruction: {current_instruction}, Stage: {current_stage}, State: {current_state}, Minute: {current_minute}")
            with open("game_log.txt", "a", encoding="utf-8") as logfile:
                logfile.write(f"{datetime.now().isoformat()} | Spiel: {current_game}, Minute: {current_minute}, No: {current_no}, Instruction: {current_instruction}, Stage: {current_stage}, State: {current_state}\n")

if __name__ == "__main__":
    print("Monitoring gestartet...")
    while True:
        if is_within_allowed_time():
            message = monitor_dingtalk(region=region)
            process_message(message)
        else:
            current_game = current_state = current_no = current_stage = current_instruction = current_minute = last_no = None
        time.sleep(interval)
