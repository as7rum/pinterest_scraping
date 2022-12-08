from config import API_TOKEN
from messages import start_message, darling_message
import asyncio
import logging
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.filters.text import Text

logging.basicConfig(level =logging.INFO)

bot = Bot(token = API_TOKEN)
dp = Dispatcher()

list_of_images = []
current_sending_page = 1
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

def get_five_photos():

    global list_of_images
    global current_sending_page
    
    start_index = (current_sending_page-1) * COUNT_FOR_SENDING
    images = list_of_images[start_index:start_index + COUNT_FOR_SENDING]
    current_sending_page += 1

    return images

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(start_message)

@dp.message(Text(text="дарлинг", ignore_case=True))
async def darling(message: types.Message):
    await message.answer(darling_message)

@dp.message(Text(text="еще", ignore_case=True))
async def send_other_photos(message: types.Message):
    global sleep_timer
    global limit
    global current_sending_page

    if list_of_images == []:
        await message.answer('Вы еще ничего не искали!')
    else:
        if get_five_photos() == []:
            sleep_timer += 1
            limit += 20
            get_images(pin_request_input, sleep_timer, limit)
        current_sending_page -= 1
        images_link = get_five_photos()
        map_images_link = list(map(lambda x: types.InputMediaPhoto(media = x), images_link))
        await message.answer('Еще '+pin_request_input) 
        await message.answer_media_group(map_images_link)


@dp.message()
async def send(message: types.Message):

    result_message = message.text.lower()

    global sleep_timer
    global limit
    global current_sending_page
    global pin_request_input

    pin_request_input = message.text
    current_sending_page = 1
    get_images(message.text, sleep_timer, limit)
    images_link = get_five_photos()
    map_images_link = list(map(lambda x: types.InputMediaPhoto(media = x), images_link))
    await message.answer(pin_request_input)
    await message.answer_media_group(map_images_link)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())