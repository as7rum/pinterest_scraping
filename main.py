from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import os
import pandas as pd

# try:
#     os.chdir(os.path.join(os.getcwd(), 'images'))
# except:
#     pass

list_of_images = []
current_sending_page = 2
COUNT_FOR_SENDING = 5

scroll_num = 20
sleep_timer = 1
var = 'машины'
limit = 20

def get_images(var, sleep_timer, limit):

    url = f'https://ru.pinterest.com/search/pins/?q={var}'

    options = webdriver.ChromeOptions()  
    options.add_argument('--blink-settings=imagesEnabled=false') 
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
    driver.maximize_window()
    driver.get(url)
    driver.execute_script(f"document.body.style.zoom='{1}%'")
    driver.execute_script("window.dispatchEvent(new Event('resize'));")

    time.sleep(sleep_timer)

    # for i in range(1, scroll_num):
    #    driver.execute_script('window.scrollTo(1, 100000)')
    #    print ('scroll-down')
    #    time.sleep(sleep_timer)
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    for object in soup.findAll('img', limit=limit):

        link = object.get('src').replace('236x', '736x')
        if link not in list_of_images:
            list_of_images.append(link)

        # with open('images/' + names_of_images.replace('/', ' ')+'.png', 'wb') as file:
        #     image = requests.get(link)
        #     file.write(image.content)
    return list_of_images[:5]

def send_five_photos():

    images_array = list_of_images  #get_images(var, sleep_timer, limit)
    global current_sending_page
    print(current_sending_page)
    
    start_index = (current_sending_page-1) * COUNT_FOR_SENDING
    images = images_array[start_index:start_index + COUNT_FOR_SENDING]
    current_sending_page += 1

    return images

if __name__ == '__main__':
     while True:
        user_input = input('''
        Введите ваш запрос, чтобы получить по нему картинки.
        Если вы хотите получить больше картинок, введите "еще".
        Если вы хотите завершить программу, введите "стоп"
        ''')
        if user_input == 'стоп':
            break
        if user_input == 'еще':
            if list_of_images == []:
                print('вы еще ничего не искали!')
                current_sending_page = 2
            else:
                print(send_five_photos())
        if user_input != 'еще':
            current_sending_page = 2
            print(get_images(user_input, sleep_timer, limit))
    #     user_input = input("Напишите next для продолжения: ")
    #     if user_input == 'next':
    #         print(send_five_photos())