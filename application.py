import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


from crawl import any_of_elements_present


def crawl(crawler):
    url = "https://hub.docker.com/layers/pytorch/pytorch/0.4_cuda9_cudnn7/images/sha256-2a25af68b37a33881e6e41dfa663291e39fac784d9453dfa26be918fb57d25e5?context=explore"
    crawler.get_url(url)
    
    WebDriverWait(crawler.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler'))
    )
    crawler.crawl_item(By.CSS_SELECTOR, 'button#onetrust-accept-btn-handler').click()
    
    WebDriverWait(crawler.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@data-testid="imglayersLayerListItem"]'))
    )
    
    layers = crawler.crawl_items(By.XPATH, '//div[@data-testid="imglayersLayerListItem"]')
    for layer in layers:
        layer.click()
        detail = crawler.crawl_item(By.XPATH, '//div[@data-testid="imglayersLayerInstruction"]/div[2]/div/div')
        print("Layer: ")
        print(layer.find_element(By.XPATH, 'div[2]').text.strip())
        print("Command: ")
        print(detail.text.strip())
        print()
        time.sleep(1)