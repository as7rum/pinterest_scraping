from config import API_TOKEN
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot)

list_of_images = []
current_sending_page = 2
COUNT_FOR_SENDING = 5

scroll_num = 20
sleep_timer = 1#+=sleep_timer
limit = 20#+=limit

def get_images(var, sleep_timer, limit):

    global list_of_images
    list_of_images = []

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

    return list_of_images[:5]

def send_five_photos():

    images_array = list_of_images
    global current_sending_page
    
    start_index = (current_sending_page-1) * COUNT_FOR_SENDING
    images = images_array[start_index:start_index + COUNT_FOR_SENDING]
    current_sending_page += 1

    return images

@dp.message_handler(commands = ['start'])
async def start_command(message: types.Message):
    await message.answer('''Привет, меня зовут A\V/ или AIVI (Artifical Intelegence Version 1).
Да, как оказалось во всем есть смысл... К сожалению, функция погоды пока недоступна, но Айнар активно над этим работает.
Но пока я могу отправить тебе картинки. Введи тему в сообщении. 
Если тебе захочится больше картинок, то введи "еще" (с маленькой буквы и без "ё") или введи новый запрос. 
Ну что? Попробуем?✨''')

@dp.message_handler()
async def send(message: types.Message):

    message.text = message.text.lower()

    global sleep_timer
    global limit
    global list_of_images
    global current_sending_page
    global pin_request_input

    if message.text == 'дарлинг':
        await message.answer("""И все же ты солнышко, май литл стар✨ 
Я тоже подумал, что пасхалки должны оставаться""")
        return

    if message.text != 'еще':
        pin_request_input = message.text
        current_sending_page = 2
        images_link = get_images(message.text, sleep_timer, limit)
        map_images_link = list(map(lambda x: types.InputMediaPhoto(x), images_link))
        await message.answer(pin_request_input)
        await message.answer_media_group(map_images_link)

    if message.text == 'еще':
        if list_of_images == []:
            await message.answer('вы еще ничего не искали!')
        else:
            if send_five_photos() == []:
                sleep_timer += 1
                limit += 20
                get_images(pin_request_input, sleep_timer, limit)
            current_sending_page -= 1
            images_link = send_five_photos()
            map_images_link = list(map(lambda x: types.InputMediaPhoto(x), images_link))
            await message.answer('еще '+pin_request_input) 
            await message.answer_media_group(map_images_link)


if __name__ == '__main__':
    executor.start_polling(dp)
