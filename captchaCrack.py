from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import cv2
import ddddocr
import time
import numpy as np
import io

TARGET_URL = r"https://csms.mohw.gov.tw/lcms/"  # 目標URL
ocr = ddddocr.DdddOcr()                         # 初始化 ddddocr

# 這裡用RemoteDriver是因為剛好有 請選擇用自己有的driver 例如 webdriver.chrome(...)
PATH = "C:/Users/astus/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get(TARGET_URL)  # 載入網頁
wait = WebDriverWait(driver, 10)  # 設定implicit wait 為10秒

# 有個礙事的modal 直接用javascript幹掉他
modal: WebElement = wait.until(
    EC.visibility_of_element_located((By.ID, "myModal")))
driver.execute_script("arguments[0].remove();", modal)

# 因為驗證碼固定長度為4個字元 為了提高準確度
# 辨識結果的字串長度不為4時 重新取的新的驗證
# 碼 這邊寫成function方便呼叫


def captchaCrack(driver: webdriver) -> str:
    wait = WebDriverWait(driver, 10)
    # 找驗證碼圖片
    captchaDiv: WebElement = wait.until(
        EC.visibility_of_element_located((By.ID, "captchaDiv")))
    captchaImg: WebElement = captchaDiv.find_element_by_tag_name("img")
    #captchaImg: WebElement = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div/form/div[3]/div/span/img")

    # 截圖存成PIL的Image
    img = Image.open(io.BytesIO(captchaImg.screenshot_as_png))
    # 灰階處理
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    # 雜訊處理
    noise = np.random.normal(0, 15, threshold.shape)
    noise = np.clip(threshold +noise, 0, 255).astype('uint8')
    guassian = cv2.blur(noise, (3, 3))
    # 最後存回 PIL Image
    img = Image.fromarray(guassian)
    # 回傳辨識結果
    return ocr.classification(img)


res = captchaCrack(driver)
# 如果長度不為4 點擊重新整理再辨識一次
while(len(res) != 4):
    refresh: WebElement = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[text()='重新產生']")))
    refresh.click()
    time.sleep(1)
    res = captchaCrack(driver)

# 接著找驗證碼的input
captcha_input: WebElement = wait.until(
    EC.visibility_of_element_located((By.ID, "captcha")))

# 將結果輸入到input
captcha_input.send_keys(res)


# 無窮迴圈，保持程式運行
while True:
    pass