import time
import re
import sys
from datetime import datetime

import requests
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from .config import CHROMEDRIVER_PATH
from .config import DESIRED_DATE
from .config import DISCORD_WEBHOOK_URL_HEARTBEAT
from .config import DISCORD_WEBHOOK_URL_TICKETS
from .config import TARGET_URL


## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")

# Set path to chromedriver as per your configuration
webdriver_service = Service(CHROMEDRIVER_PATH)

# Choose Chrome Browser
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)


# E.g. Friday 6th October 2023
DATE_REGEX = r'\w+ \d+\w+ \w+ \d+'
DESIRED_DATE_REGEX = rf"\b{DESIRED_DATE}\b"


def post_to_discord(webhook_url: str, content: str) -> None:
    data = {'content': content}
    response = requests.post(webhook_url, json=data)
    print('Status:', response.status_code)
    response.raise_for_status()


def run_once(class_: str) -> None:
    print('loading', TARGET_URL)
    browser.get(TARGET_URL)
    # TODO: early exit if page failed to load
    print('successfully loaded', TARGET_URL)

    # specify adults
    element = browser.find_element(By.NAME, "adults")
    element.send_keys(Keys.BACK_SPACE)
    element.send_keys("2")
    element.send_keys(Keys.RETURN)
    print('Adult value:', element.get_attribute('value'))

    # specify children
    element = browser.find_element(By.NAME, "children")
    element.send_keys(Keys.RIGHT)
    element.send_keys(Keys.BACK_SPACE)
    element.send_keys("0")
    element.send_keys(Keys.RETURN)
    print('Children value:', element.get_attribute('value'))

    # specify ticket class (drop down menu)
    element = browser.find_element(By.NAME, "class")
    s = Select(element)
    s.select_by_visible_text(class_)
    print('Class value:', element.get_attribute('value'))

    find_trips = browser.find_element(
        By.XPATH,
        '/html/body/div[3]/section[1]/div/div[2]/div[4]/button'
    )
    print('clicking', find_trips.text)
    find_trips.click()

    # TODO: improve this need to sleep
    time.sleep(5)

    elements = browser.find_elements(By.CLASS_NAME, 'w-full')
    # filter for only elements containing dates
    # apparently this call is expensive...
    elements = [e for e in elements if re.search(DATE_REGEX, e.text)
                and len(e.text.splitlines()) == 3]
    print('looping through elements')
    print(f'{len(elements)} dates found')

    for e in elements:
        date, time_, status = e.text.splitlines()
        if status == 'SOLD OUT':
            continue

        if not re.search(DESIRED_DATE_REGEX, date):
            continue

        print('Available!')
        return True

    # Date not available :(
    print('Not available :(')
    return False


def main() -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        available_classes = []
        for class_ in ["First Class", "First Class - Table for 2", "Standard Class"]:
            is_available = run_once(class_)
            if is_available:
                available_classes.append(class_)

        if available_classes:
            content = f'Tickets available for {DESIRED_DATE} in {available_classes}'
            post_to_discord(DISCORD_WEBHOOK_URL_TICKETS, content)
        else:
            content = f'[{timestamp}] Run succeeded but no tickets available'
            post_to_discord(DISCORD_WEBHOOK_URL_HEARTBEAT, content)

    except Exception as exc:
        print('Ecountered exception:', exc)
        content = f'[{timestamp}] Encountered exception: {exc}'
        post_to_discord(DISCORD_WEBHOOK_URL_HEARTBEAT, content)


if __name__ == '__main__':
    main()
