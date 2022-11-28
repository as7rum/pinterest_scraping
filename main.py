from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import os

# try:
#     os.chdir(os.path.join(os.getcwd(), 'images'))
# except:
#     pass

scroll_num = 20
sleep_timer = 10
var = 'машины'
url = f'https://ru.pinterest.com/search/pins/?q={var}'


options = webdriver.ChromeOptions()  
options.add_argument('--blink-settings=imagesEnabled=false') 
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
driver.maximize_window()
driver.get(url)
driver.execute_script(f"document.body.style.zoom='{100}%'")
driver.execute_script("window.dispatchEvent(new Event('resize'));")
time.sleep(sleep_timer)

# for i in range(1, scroll_num):
#     driver.execute_script('window.scrollTo(1, 100000)')
#     print ('scroll-down')
#     time.sleep(sleep_timer)
    

soup = BeautifulSoup(driver.page_source, 'html.parser')

image_number = 0

for link in soup.findAll('img'):
    names_of_images = link.get('src').strip('https://i.pinimg.com/236x/db/2b/7e/.jpg')
    links = link.get('src').replace('236x', '736x')

    image_number += 1

    with open('images/' + names_of_images.replace('/', ' ')+'.png', 'wb') as file:
        image = requests.get(links)
        file.write(image.content)

print(image_number)