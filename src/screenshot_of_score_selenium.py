from selenium import webdriver
from selenium.webdriver import ChromeOptions

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


from PIL import Image
import os
import time

# Takes screenshot of the score from osu! website
def screenshot_of_score(score_url: str):
    start_time = time.time()
    # Start Webdriver
    opts = ChromeOptions()
    opts.add_argument("headless")
    opts.add_argument("--window-size=1050,1000")
    
    driver = webdriver.Chrome(options=opts)
    driver.get(score_url)
    
    try:
        WebDriverWait(driver, 10).until(
            lambda d: d.execute_script("return Array.from(document.images).every(img => img.complete)")
        )
    except TimeoutException:
        print("Timed out waiting for images to load")
        driver.quit()
        return
    
    time.sleep(1)
    
    # Take screenshot of score info
    driver.save_screenshot("screenshot.png")
    driver.quit()
    screenshotted = Image.open("screenshot.png")

    # Dimensions of screenshot to only include
    # score info
    left = 20
    top = 105
    right = 1004
    bottom = 636    

    # Crop, save, and delete non-cropped screenshot
    cropped = screenshotted.crop((left, top, right, bottom))
    cropped.save(f"flaskr/static/score.png")
    os.remove("screenshot.png")
    print("Score screenshot Ready!")
    end_time = time.time()
    print(end_time - start_time)


screenshot_of_score("https://osu.ppy.sh/scores/1674443338")