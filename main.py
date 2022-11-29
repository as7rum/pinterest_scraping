from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

list_of_images = []
current_sending_page = 2
COUNT_FOR_SENDING = 5

scroll_num = 20
sleep_timer = 1#+=sleep_timer
limit = 20#+=limit

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
        if user_input != 'еще':
            pin_request_input = user_input
            current_sending_page = 2
            images_link = get_images(user_input, sleep_timer, limit)
            for image_link in images_link:
                with open('images/' + image_link.split('/')[-1], 'wb') as file:
                    image = requests.get(image_link)
                    file.write(image.content)
        if user_input == 'еще':
            if list_of_images == []:
                print('вы еще ничего не искали!')
            else:
                if send_five_photos() == []:
                    sleep_timer += 1
                    limit += 20
                    get_images(pin_request_input, sleep_timer, limit)
                current_sending_page -= 1
                images_link = send_five_photos()
                for image_link in images_link:
                    with open('images/' + image_link.split('/')[-1], 'wb') as file:
                        image = requests.get(image_link)
                        file.write(image.content)
    #     user_input = input("Напишите next для продолжения: ")
    #     if user_input == 'next':
    #         print(send_five_photos())