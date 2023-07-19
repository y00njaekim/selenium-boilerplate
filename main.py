from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


class DriverSingleton:
    _instance = None

    def __new__(cls, headless: bool = False):
        if cls._instance is None:
            chrome_driver_manager = ChromeDriverManager().install()
            if headless:
                headlessoptions = webdriver.ChromeOptions()
                headlessoptions.add_argument('headless')
                headlessoptions.add_argument('window-size=1920x1080')
                headlessoptions.add_argument('disable-gpu')
                agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
                headlessoptions.add_argument(agent)
                headlessoptions.add_argument('lang=ko_KR')
                driver = webdriver.Chrome(
                    options=headlessoptions, service=Service(chrome_driver_manager))
            else:
                driver = webdriver.Chrome(
                    service=Service(chrome_driver_manager))
            cls._instance = driver
        return cls._instance


def get_driver(headless: bool = False):
    return DriverSingleton(headless)


def crawl(by, query, url: str):
    driver = get_driver()
    try:
        driver.get(url)
    except:
        print("Failed to connect to URL:", url)
        return []
    ret = preprocess(driver.find_elements(by, query))
    return ret


def preprocess(elems):
    elems = [elem.text for elem in elems]
    return elems


def main():
    by = By.CSS_SELECTOR
    query = "div[data-testid='imglayersLayerListItem'] div.styles__instruction___PSEJc"
    url = 'https://hub.docker.com/layers/lambci/lambda/20210129-build-python3.8/images/sha256-22e9fbb4df8270efcebed96905edf0244dd595a8d6250f24200ad558c0a201bc'

    ret = crawl(by, query, url)

    print(ret)
    return ret


if __name__ == "__main__":
    main()
