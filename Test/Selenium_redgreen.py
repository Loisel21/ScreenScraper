from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from a_selenium_click_on_coords import click_on_coordinates


def main():
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

        element = driver.find_element(By.CSS_SELECTOR, ".RG:nth-child(5) > .\\__cover") #3 minute red green
        driver.execute_script("arguments[0].scrollIntoView();", element)
        driver.find_element(By.CSS_SELECTOR, ".RG:nth-child(5) > .\\__cover").click() #3 minute red green
        
        time.sleep(3)

        driver.execute_script("window.scrollTo(0,0)")
        time.sleep(3)

        driver.find_element(By.CSS_SELECTOR, ".input").click()
        driver.find_element(By.CSS_SELECTOR, ".input").send_keys("0.1")
        driver.find_element(By.CSS_SELECTOR, ".betDiv:nth-child(1) > .label").click()
        driver.find_element(By.CSS_SELECTOR, ".betBtn").click()
        driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
            
        #Cancel bet
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, ".dot").click()
        driver.find_element(By.CSS_SELECTOR, ".itemBox > .item:nth-child(2)").click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, ".Rebut").click()
        time.sleep(3)
        driver.find_element(By.CSS_SELECTOR, ".btn-submit").click()
        time.sleep(3)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
