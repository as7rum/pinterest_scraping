from config import API_TOKEN

while True:
        user_input = input('''
        Введите ваш запрос, чтобы получить по нему картинки.
        Если вы хотите получить больше картинок, введите "еще".
        Если вы хотите завершить программу, введите "стоп"
        ''')
        if user_input == 'еще':
            print('отправляем еще фоточек')
        if user_input == 'стоп':
            break
        if user_input != 'еще':
            print('ваш запрос', user_input)
        # else:
        #     pass