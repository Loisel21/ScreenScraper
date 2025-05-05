from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from a_selenium_click_on_coords import click_on_coordinates


def execute_bet(game, minute, instruction, last_balance, bet_steps):
    # Mobiler iPhone-User-Agent
    mobile_user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.3 Mobile/15E148 Safari/604.1"

    # Firefox-Optionen konfigurieren
    options = Options()
    options.set_preference("general.useragent.override", mobile_user_agent)
    # options.add_argument("--headless")  # Falls du headless willst

    # WebDriver starten
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1654, 1034)

    try:
        # Webseite öffnen
        driver.get("https://m.play2riches.com/login?backUrl=%2FuserCenter")

        # Login
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, ".user-input").click()
        driver.find_element(By.CSS_SELECTOR, ".user-input").send_keys("Loiseloni")
        driver.find_element(By.CSS_SELECTOR, ".formItem:nth-child(3) > .input").send_keys("nE8H*t1&biBO#k*4")
        driver.find_element(By.CSS_SELECTOR, ".loginBtn").click()

        time.sleep(3)

        click_on_coordinates(driver,x=100,y=100, script_timeout=10)

        time.sleep(1)

        driver.find_element(By.CSS_SELECTOR, "p > .svg-icon").click()
        time.sleep(1)



        game_element, instruction_button = get_game_elements(game, minute, instruction)

        if game_element is None:
            print("Invalid game or minute specified.")
            return

        element = driver.find_element(By.CSS_SELECTOR, game_element)
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.find_element(By.CSS_SELECTOR, game_element).click()

        time.sleep(3)

        balance_element = driver.find_element(By.CSS_SELECTOR, ".balance").text
        current_balance = float(balance_element.split()[0])

        if last_balance == 0.0:
            last_balance = current_balance
        elif current_balance > last_balance:
            bet_index = 0
        elif current_balance < last_balance:
            bet_index = min(bet_index + 1, len(bet_steps) - 1)

        

        
        driver.execute_script("window.scrollTo(0,0)")
        time.sleep(3)

        driver.find_element(By.CSS_SELECTOR, instruction_button).click()

        driver.find_element(By.CSS_SELECTOR, ".input").click()

        #LNO Calculate Bet Steps
        driver.find_element(By.CSS_SELECTOR, ".input").send_keys(bet_steps[bet_index])

        driver.find_element(By.CSS_SELECTOR, ".betBtn").click()
        driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
            
        #Cancel bet
        time.sleep(5)
        driver.find_element(By.CSS_SELECTOR, ".dot").click()
        driver.find_element(By.CSS_SELECTOR, ".itemBox > .item:nth-child(2)").click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, ".Rebut").click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
        time.sleep(3)

    finally:
        driver.quit()

def get_game_elements(game, minute, instruction):
    if game == "redgreen":
        match minute:
            case 3:
                game_element = ".RG:nth-child(5) > .\\__cover"
                match instruction:
                    case "red": instruction_button = ".betDiv:nth-child(1)"
                    case "green": instruction_button = ".betDiv:nth-child(3)"
            
    if game == "blocks":
        match minute:
            case 3:
                game_element = ".BLK:nth-child(4) > .\\__cover"
                match instruction:
                    case "odd": instruction_button = ".betDiv:nth-child(3)"
                    case "even": instruction_button = ".betDiv:nth-child(4)"
            
    if game == "discs":
        match minute:
            case 3:
                game_element = ".DS:nth-child(6) > .\\__cover"
                match instruction:
                    case "odd": instruction_button = ".betDiv:nth-child(2)"
                    case "even": instruction_button = ".betDiv:nth-child(5)"

    return game_element, instruction_button

if __name__ == "__main__":
    execute_bet(game = "redgreen", minute = 3, instruction = "green", last_balance = 0.0, bet_steps = [0.1, 0.3, 0.9, 2.7, 8.1, 24.3, 72.9, 218.7])
