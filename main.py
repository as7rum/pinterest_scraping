from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import os

try:
    os.chdir(os.path.join(os.getcwd(), 'images'))
except:
    pass

scroll_num = 1
sleep_timer = 1

var = 'блестящий маникюр'
url = f'https://ru.pinterest.com/search/pins/?q={var}'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
driver.get(url)

for _ in range(1, scroll_num):
    driver.execute_scripting('window.scrollTo(1, 100000)')
    print ('scroll-down')
    time.sleep(sleep_timer)

soup = BeautifulSoup(driver.page_source, 'html.parser')

for link in soup.findAll('img'):
    names_of_images = link.get('src').strip('https://i.pinimg.com/236x/db/2b/7e/.jpg')
    links = link.get('src')

    with open(names_of_images.replace('/', ' ')+'.png', 'wb') as file:
        image = requests.get(links)
        file.write(image.content)