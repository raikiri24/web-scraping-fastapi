from fastapi import FastAPI
from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from fastapi_utils.tasks import repeat_every

app = FastAPI()


@app.on_event("startup")
@repeat_every(seconds=60 * 1)  # 1 hour
def remove_expired_tokens_task() -> None:
    driver = webdriver.Firefox()
    driver.get("https://shopee.ph/flash_deals?promotionId=180932244078593")
    delay = 25 # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'hSM8kk')))
        print("Page is ready!")
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        all_names = [e.text for e in soup.find_all("div", {"class": "ne3HDa"})]
        all_prices = [e.text for index,e in  enumerate(soup.find_all("div", {"class": "hSM8kk"})) if index % 2 != 0]
        merged_list = [{'price': price, 'item': item} for price, item in zip(all_prices, all_names)]
        print(f"{merged_list}")
    except:
        print("Loading took too much time!")

@app.get("/")
async def root():
    return {"message": "hello"}
    
   
