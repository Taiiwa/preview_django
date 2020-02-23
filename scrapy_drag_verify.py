from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time

browser = webdriver.Chrome()

url = 'http://127.0.0.1:8080/login/'

browser.get(url)

# 输入账号密码
username = browser.find_element_by_xpath('//*[@id="app"]/div/section/div[1]/input')
username.send_keys('123')

password = browser.find_element_by_xpath('//*[@id="app"]/div/section/div[2]/input')
password.send_keys('123')

# 外框的坐标
square = browser.find_element_by_xpath('//*[@id="app"]/div/section/div[3]/center/div/div/div[2]')

# 滑块的长度
drag_button = browser.find_element_by_xpath('//*[@id="app"]/div/section/div[3]/center/div/div/div[3]')
drag_button_len = drag_button.size.get('width')


# 滑动条的长度
square_len = square.size.get('width')

# 终止x坐标
end_x = int(square_len - drag_button_len)
print((end_x, y))

time.sleep(1)

# 定义模拟动作
action = ActionChains(browser)

# 拖拽滑块
action.drag_and_drop_by_offset(drag_button, end_x, 0)
action.perform()


time.sleep(1)
submit = browser.find_element_by_xpath('//*[@id="app"]/div/section/div[4]/button')

submit.click()
