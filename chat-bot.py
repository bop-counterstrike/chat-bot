import telebot
import config
import sqlite3
from telebot import types

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['admin'])
def admin(message):
    bot.send_message(message.chat.id, 'Введи код доступа')
    bot.register_next_step_handler(message, password)
def password(message):
    if message.text == 'qwerty12345':
        bot.send_message(message.chat.id, 'Код доступа верный', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, work_list)
    else:
        bot.send_message(message.chat.id, 'Код доступа неверный', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, admin)

def work_list(message):
    conn = sqlite3.connect('bd.sql')
    cur = conn.cursor()
    cur.execute("""SELECT wl.dt_date, wl.dt_time, cl.first_name, cl.last_name, cl.phone_n 
    FROM work_list wl, clients cl
    WHERE wl.cl_number = cl.phone_n""")
    people = cur.fetchall()
    info = ''

    for el in people:
        info += f'{el[0]} - {el[1]} - {el[2]} - {el[3]} - {el[4]}\n'

    cur.close()
    conn.close()

    bot.send_message(message.chat.id, info)
    bot.send_message(message.chat.id, 'Отправь любое сообщение, чтобы вернуться в начало')
    bot.register_next_step_handler(message, start)
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Запись на процедуру')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Как добраться?')
    btn3 = types.KeyboardButton('Цены')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, 'Привет! Я-бот, который поможет тебе записаться на маникюр! Выбери один из пунктов ниже)', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def on_click(message):
    if message.text == 'Запись на процедуру':
        bot.send_message(message.chat.id, 'Окей, тогда введи свое имя', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, first_name)
    elif message.text == 'Как добраться?':
        bot.send_message(message.chat.id, f'Очень просто! Адрес: г. Дубна, ул. Макаренко, д. 21А, офис "Samira", остановка "Магазин Атак", вход с торца здания\n Введи любое сообщение, чтобы вернуться в начало', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, start)
    elif message.text == 'Цены':
        conn = sqlite3.connect('bd.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM prices")
        prices = cur.fetchall()

        info = ''

        for el in prices:
            info += f'{el[0]} - {el[1]}\n'

        cur.close()
        conn.close()
        bot.send_message(message.chat.id, info, reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, 'Отправь любое сообщение, чтобы вернуться в начало')
        bot.register_next_step_handler(message, start)

f_name = None
l_name = None
phone = None
def first_name(message):
    global f_name
    f_name = message.text.strip()
    bot.send_message(message.chat.id, 'Отлично! Теперь напиши свою фамилию!')
    bot.register_next_step_handler(message, last_name)
def last_name(message):
    global l_name
    l_name = message.text.strip()
    bot.send_message(message.chat.id, 'Получил, теперь введи номер телефона в формате 9ХХХХХХХХХ(без +7 или 8)')
    bot.register_next_step_handler(message, phone_number)

free_dates = None
free_date_1 = None
free_date_2 = None
free_date_3 = None
free_date_4 = None
free_date_5 = None

"""def phone_check(message):
    global phone
    phone = message.text.strip()
    if len(phone) != 10:
        bot.send_message(message.chat.id, 'Введи номер корректно')
        bot.register_next_step_handler(message, phone_check)
    else:
        bot.register_next_step_handler(message, phone_number)"""
def phone_number(message):
    global phone
    global free_dates
    global free_date_1
    global free_date_2
    global free_date_3
    global free_date_4
    global free_date_5
    #get phone
    phone = message.text.strip()
    conn = sqlite3.connect('bd.sql')
    cur = conn.cursor()
    #get free dates for markup
    cur.execute("SELECT * FROM date_time LIMIT 5")
    free_dates = cur.fetchall()
    free_date_1 = free_dates[0]
    free_date_2 = free_dates[1]
    free_date_3 = free_dates[2]
    free_date_4 = free_dates[3]
    free_date_5 = free_dates[4]
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(f'{free_date_1}', callback_data='date_1')
    btn2 = types.InlineKeyboardButton(f'{free_date_2}', callback_data='date_2')
    markup.row(btn1,btn2)
    btn3 = types.InlineKeyboardButton(f'{free_date_3}', callback_data='date_3')
    btn4 = types.InlineKeyboardButton(f'{free_date_4}', callback_data='date_4')
    markup.row(btn3, btn4)
    btn5 = types.InlineKeyboardButton(f'{free_date_5}', callback_data='date_5')
    markup.row(btn5)
    #phone check
    cur.execute(f"SELECT phone_n FROM clients WHERE phone_n = {phone}")
    data = cur.fetchone()
    if data is None:
        cur.execute(f"INSERT INTO clients(phone_n, first_name, last_name) VALUES ('{phone}', '{f_name}', '{l_name}')")
        bot.send_message(message.chat.id, 'Так, вижу, что в первый раз.. Ну, тогда добро пожаловать! Осталось выбрать дату и время)', reply_markup=markup)
    else:
        bot.send_message(message.chat.id,'Так ты у нас не впервые! Снова безумно рад видеть! Выбирай дату и время', reply_markup=markup)
    conn.commit()
    cur.close()
    conn.close()
#обработка кнопок
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    global f_name
    global l_name
    global phone
    global free_date_1
    global free_date_2
    global free_date_3
    global free_date_4
    global free_date_5
    conn = sqlite3.connect('bd.sql')
    cur = conn.cursor()
    if callback.data == 'date_1':
        final_date = free_date_1[0]
        final_time = free_date_1[1]
    elif callback.data == 'date_2':
        final_date = free_date_2[0]
        final_time = free_date_2[1]
    elif callback.data == 'date_3':
        final_date = free_date_3[0]
        final_time = free_date_3[1]
    elif callback.data == 'date_4':
        final_date = free_date_4[0]
        final_time = free_date_4[1]
    elif callback.data == 'date_5':
        final_date = free_date_5[0]
        final_time = free_date_5[1]
    print(final_time, final_date)
    cur.execute(f"INSERT INTO work_list(cl_number, dt_date, dt_time) VALUES('{phone}','{final_date}','{final_time}')")
    cur.execute(f"DELETE FROM date_time WHERE date_ = '{final_date}' AND time_ = '{final_time}'")
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(callback.message.chat.id, f'Успешно!Записали тебя на {final_date} в {final_time}\n Отправь любое сообщение, чтобы вернуться в начало')
    bot.register_next_step_handler(callback.message, start)

bot.polling(none_stop=True)
