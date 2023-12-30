import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


from crawl import any_of_elements_present


def get_access_token(crawler, email, passwd):
    url = "https://accounts.fitbit.com/login?targetUrl=https%3A%2F%2Fdev.fitbit.com%2Flogin%2Ftransferpage%3Fredirect%3Dhttps%253A%252F%252Fdev.fitbit.com%252Fapps"
    crawler.get_url(url)
    WebDriverWait(crawler.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )

    email_input = crawler.crawl_item(
        By.CSS_SELECTOR, 'input[type="email"]', is_preprocess=False
    )
    email_input.clear()
    email_input.send_keys(email)
    time.sleep(1)

    password_input = crawler.crawl_item(
        By.CSS_SELECTOR, 'input[type="password"]', is_preprocess=False
    )
    password_input.clear()
    password_input.send_keys(passwd)
    time.sleep(1)

    password_input.send_keys(Keys.ENTER)

    WebDriverWait(crawler.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.name"))
    )

    application = crawler.crawl_item(By.CSS_SELECTOR, "a.name")
    application.click()

    app_property_blocks = crawler.crawl_items(By.CSS_SELECTOR, "div.appPropertyBlock")

    client_id = ""
    client_secret = ""
    for block in app_property_blocks:
        name_elem = block.find_element(By.CLASS_NAME, "name")
        value_elem = block.find_element(By.CLASS_NAME, "value")

        if name_elem.text == "OAuth 2.0 Client ID":
            client_id = value_elem.text
        elif name_elem.text == "Client Secret":
            client_secret = value_elem.text

    token_url = f"https://www.fitbit.com/oauth2/authorize?response_type=token&client_id={client_id}&redirect_uri=http://127.0.0.1:8080/&expires_in=31536000&scope=activity+nutrition+heartrate+location+nutrition+profile+settings+sleep+social+weight"
    crawler.get_url(token_url)

    WebDriverWait(crawler.driver, 10).until(
        any_of_elements_present(
            [
                (By.CSS_SELECTOR, "div#offline-resources"),
                (By.CSS_SELECTOR, "span.allow-all-checkbox"),
            ]
        )
    )

    try:
        allow_check_box = crawler.crawl_item(By.CSS_SELECTOR, "span.allow-all-checkbox")
        allow_check_box.click()
        allow_button = crawler.crawl_item(By.CSS_SELECTOR, "button.allow-button")
        allow_button.click()
        WebDriverWait(crawler.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div#offline-resources"))
        )
    except NoSuchElementException:
        pass

    token = crawler.driver.current_url
    token = token.split("access_token=")[1].split("&")[0]

    logout_url = "https://dev.fitbit.com/apps"
    crawler.get_url(logout_url)
    WebDriverWait(crawler.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#cust > ul > li.last > a"))
    )

    logout_button = crawler.crawl_item(By.CSS_SELECTOR, "#cust > ul > li.last > a")
    logout_button.click()
    WebDriverWait(crawler.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
    )

    return client_id, client_secret, token
