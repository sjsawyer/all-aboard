from selenium import webdriver


# TODO: more generic type than Chrome
def save_screenshot(browser: webdriver.Chrome) -> None:
    with open('img.png', 'wb') as f:
        f.write(browser.get_screenshot_as_png())

