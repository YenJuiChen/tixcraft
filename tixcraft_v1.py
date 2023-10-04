from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from PIL import Image
import cv2
import ddddocr
import time
import numpy as np
import io
import pyautogui

options = webdriver.ChromeOptions()
prefs = {
    'profile.default_content_setting_values':
        {
            'notifications': 2
        }
}
options.add_experimental_option('prefs', prefs) 
options.add_argument("disable-infobars") 

PATH = "C:/Users/astus/Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.maximize_window() 
wait = WebDriverWait(driver, 10)  # 最長等待時間為 10 秒

driver.get("https://tixcraft.com/") # 到搶票網頁頁面
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="onetrust-accept-btn-handler"]').click() #接受cookie


driver.find_element(By.XPATH,'//*[@id="bs-navbar"]/div/div[2]/ul[3]/li/a/span').click() #點擊登陸按鈕
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="loginFacebook"]').click()  #FB快速登入


account = driver.find_element(By.XPATH,'//*[@id="email"]')
account.clear()
account.send_keys('pig7745@yahoo.com.tw')
password = driver.find_element(By.XPATH,'//*[@id="pass"]')
password.clear()
password.send_keys('kai111486')
driver.find_element(By.XPATH,'//*[@id="loginbutton"]').click() #點擊登入按鈕
time.sleep(1)
driver.get('https://tixcraft.com/activity/detail/23_wltpe') #搶票目標@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@需修改
#driver.get('https://tixcraft.com/activity/detail/23_malone')
driver.find_element(By.XPATH,'//*[@id="tab-func"]/li[1]/a').click() #立即購票
time.sleep(2)

driver.execute_script("window.scrollBy(0,874)","")
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="gameList"]/table/tbody/tr[1]/td[4]/button').click() #立即訂購

driver.execute_script("window.scrollBy(0,874)","")#向下捲動
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="14666_38"]').click() #選區域跟價格@@@@@@@@@@@@@@@@@@@@@@@@@需修改
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="TicketForm_ticketPrice_02"]').click() #張數列表
time.sleep(1)

pyautogui.keyDown('DOWN') #這裡會直接讓他選最多四張
pyautogui.keyUp('DOWN')
pyautogui.keyDown('DOWN')
pyautogui.keyUp('DOWN')
pyautogui.keyDown('DOWN')
pyautogui.keyUp('DOWN')
pyautogui.keyDown('DOWN')
pyautogui.keyUp('DOWN')
pyautogui.keyDown('ENTER')
pyautogui.keyUp('ENTER')

ocr = ddddocr.DdddOcr()    

def captchaCrack(driver: webdriver) -> str:  #@@@@@@@@@@@@@@@@@@@@@@@@@@@@需要優化
    wait = WebDriverWait(driver, 10)
    # 找驗證碼圖片
    captchaImg: WebElement = driver.find_element(By.ID, "TicketForm_verifyCode-image")


    # 截圖存成PIL的Image
    img = Image.open(io.BytesIO(captchaImg.screenshot_as_png))
    # 灰階處理
    gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
    # 雜訊處理
    #noise = np.random.normal(0, 15, threshold.shape)
    #noise = np.clip(threshold +noise, 0, 255).astype('uint8')
    #guassian = cv2.blur(noise, (3, 3))
    # 最後存回 PIL Image
    #img = Image.fromarray(guassian)
    # 回傳辨識結果  
    return ocr.classification(img) 



res = captchaCrack(driver)
# 如果長度不為4 點擊重新整理再辨識一次
while(len(res) != 4):
    refresh: WebElement = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[1]/div[3]/div/div/div/form/div[2]/div[1]/img")))
    refresh.click()
    time.sleep(1)
    res = captchaCrack(driver)

# 接著找驗證碼的input
captcha_input: WebElement = wait.until(
    EC.visibility_of_element_located((By.ID, "TicketForm_verifyCode")))

# 將結果輸入到input
captcha_input.send_keys(res)



driver.find_element(By.ID,'TicketForm_agree').click()  #同意條款
driver.find_element(By.CLASS_NAME,'btn.btn-primary.btn-green').click()  #確認張數

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID,'CheckoutForm_paymentId_54'))
    )
except:
    print("元素未在頁面上出現，或者超時了")

driver.execute_script("window.scrollBy(0,874)","")#向下捲動
driver.find_element(By.ID,'CheckoutForm_paymentId_54').click()  #選ATM付款
#driver.find_element(By.ID,'submitButton').click()  #下一步







# 無窮迴圈，保持程式運行
while True:
    pass
