import time
import insert
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import title_contains
from selenium.webdriver.chrome.options import Options
import random
chrome_options = Options()
proxy_arr = [
     '--proxy-server=http://59.58.56.166:4780,',
     #'--proxy-server=http://43.248.136.50:20002'

]

chrome_options = Options()
proxy = random.choice(proxy_arr)  # 随机选择一个代理
print(proxy)  # 如果某个代理访问失败,可从proxy_arr中去除
chrome_options.add_argument(proxy)
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
#chrome_options.add_argument("--headless")
driver = Chrome(options=chrome_options)
driver.get("https://zhidao.baidu.com/")
#time.sleep(10)
n2 = driver.window_handles
driver.find_element(By.XPATH,'//*[@id="kw"]').send_keys("紫色毛衣搭配")
driver.find_element(By.XPATH,'//*[@id="search-btn"]').click()
while 1:
    WebDriverWait(driver,20).until(title_contains("搭配"))

    dt_list = driver.find_elements(By.CSS_SELECTOR,'dt.dt')
    for dt in dt_list:
        print(dt.text)
    for i in range(1, len(dt_list)+1):
        tt = []
        driver.find_element(By.XPATH,'//*[@id="wgt-list"]/dl[' + str(i) + ']/dt/a').click()
        #h1 = driver.find_element(By.XPATH,'//*[@id="wgt-ask"]/h1/span')
        #print(h1)
        n = driver.window_handles
        print('当前句柄: ', n)
        #driver切换至最新生产的页面
        driver.switch_to.window(n[-1])
    #    try:
    #        driver.find_element(By.XPATH,'//*[@id="best-content-4171903064"]/div[1]/div').click()
    #    except:
    #        print('111')
        try:
            q = driver.find_element(By.XPATH,'//*[@id="wgt-ask"]/h1/span')
            #WebDriverWait(driver, 5).until(title_contains("搭配"))
            a = driver.find_element(By.CLASS_NAME,'bd')
            tt.append(q.text)
            tt.append(a.text)
            print(tt)
            insert.insert(tt)
        except:
            print("失败")

        driver.close()
        driver.switch_to.window(n2[-1])
        time.sleep(1)
    print('该爬取完毕')
    print('进入下一页')

    try:
        driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/a[12]').click()
    except:
        try:
            driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/a[11]').click()
        except:
            driver.find_element(By.XPATH, '/html/body/div[4]/div[1]/div/a[10]').click()
