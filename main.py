import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time


from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

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
                driver = webdriver.Chrome(service=Service(chrome_driver_manager))
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
    query = "div#cm_cr-review_list div.a-row.a-spacing-small.review-data"

    json_data = {}
    reviews = []

    page = 1
    url = 'https://www.amazon.com/Midea-Inverter-Conditioner-Flexibility-Installation/product-reviews/B08677DCKN/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber='
    while True:
        page_url = url + str(page)
        ret = crawl(by, query, page_url)
        time.sleep(1)
        if len(ret) == 0:
            break
        reviews += ret
        page += 1
    json_data["reviews"] = reviews
    save_to_json(json_data, 'reviews.json')
    return


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
