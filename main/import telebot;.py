import telebot;
import random
import os
import sqlite3
from telebot import types

def check_reg_people(userid, chatid): #message.from_user.id and message.chat.id                  #есть id или нет
    with open(r"base/inf_people.txt", 'r', encoding='utf-8') as file:
        line = file.readline()        # считываем первую строку
        print(line, " ")

        while line != '':
            code = (line.split(":"))[0]            # пока не конец файла
            if code == str(userid):      # обрабатываем считанную строку
                return True
                #flag = True
                #break
            line = file.readline()     # читаем новую строку
        return False

def check_reg_group(userid, chatid): #message.from_user.id and message.chat.id                  #есть id или нет
    with open(r"base/inf_groups.txt", 'r', encoding='utf-8') as file:
        line = file.readline()        # считываем первую строку
        print(line, " ")

        while line != '':
            code = (line.split(":"))[0]            # пока не конец файла
            if code == str(chatid):      # обрабатываем считанную строку
                return True
                #flag = True
                #break
            line = file.readline()     # читаем новую строку
        return False
            


bot = telebot.TeleBot(token = '7736265547:AAGnxKHv45qdeeWHlMqrWE_VzGPLCnfl0fw')


@bot.message_handler(commands = ['start'])
def send_welcome(message):
    # таблица
    conn = sqlite3.connect('users.sql')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS pupols (id int auto_increment primary key, name varchar(10), role vachar(10))')
    conn.commit()
    cur.close()
    conn.close()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="ДА! Помощь нужна."))
    markup.add(types.KeyboardButton(text="Нет!"))
    #print(message.chat.id, "Привет!", reply_markup = markup)
    # Получаем список групп, в которых находится бот
    #groups = bot.chat_ids

    # Записываем список групп в файл
    #with open("chats\base\inf_chats.txt", "w") as file:
        #file.write(str(groups))

    bot.send_message(message.chat.id, f"Привет!", reply_markup = markup)


@bot.message_handler(commands = ["pup_reg_people"])
def pupi_reg_people(message):
    print((message.text).split())
    if(check_reg_people(message.from_user.id, message.chat.id)):
        bot.send_message(message.from_user.id, 'Ты уже есть в базе')
    elif len((message.text).split())==4:
        print("Уяснил")
        name = (message.text).split() #я устал пиздец
        with open("base/inf_people.txt", 'a', encoding='utf-8') as file:
            file.write(f"{message.from_user.id}:{name[1]} {name[2]} {name[3]}\n")
        if not os.path.isdir(rf"base/inf_people/{message.from_user.id}"):
            os.mkdir(rf'base/inf_people/{message.from_user.id}')

        bot.send_message(message.from_user.id, f'Привет, {name[1]} {name[2]} {name[3]}\n')
    else:
        bot.send_message(message.from_user.id, 'Напиши свое Ф.И.О')


@bot.message_handler(commands = ["pup_reg_group"])
def pupi_reg_group(message):
    print("робит?")
    number = message.chat.id
    if(check_reg_group(message.from_user.id, message.chat.id)):
        bot.send_message(message.chat.id, 'дебил?')
    else:
        with open(r"base/inf_groups.txt", 'a', encoding='utf-8') as file:
            file.write(f"{message.chat.id}:{message.text[15:]}")
        print(number)

        if not os.path.isdir(rf"base/inf_chats/{number}"):
            os.mkdir(rf'base/inf_chats/{number}')

        bot.send_message(message.chat.id, f'Привет, {number}!')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    print(f"USER: {message.from_user.id}")
    print(f"CHAT:{message.chat.id}")
    
    if check_reg_people(message.from_user.id, message.chat.id):

        if check_reg_group(message.from_user.id, message.chat.id) or message.from_user.id==message.chat.id:

            #bot.send_message(message.from_user.id, '👋 Поздороваться')

            if message.text == "ДА! Помощь нужна.":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
                btn1 = types.KeyboardButton('УЧЕНИК')
                btn2 = types.KeyboardButton('УЧИТЕЛЬ')
                btn3 = types.KeyboardButton('БИБЛИОТЕКА')
                markup.add(btn1, btn2, btn3)
                bot.send_message(message.chat.id, 'Выбирай, путник!', reply_markup=markup) #ответ бота
            if message.text == "БИБЛИОТЕКА":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(types.KeyboardButton(text="8"))
                markup.add(types.KeyboardButton(text="9"))
                markup.add(types.KeyboardButton(text="10"))
                bot.send_message(message.chat.id, 'Из какого ты класса?', reply_markup=markup)
            if message.text == "УЧЕНИК":
                bot.send_message(message.chat.id, 'Хорошо, школьник')


        
        else:
            bot.send_message(message.chat.id, 'Зарегистрируйте /pup_reg_group')


    else:
        #if message.chat.type == 'private':
        bot.send_message(message.from_user.id, 'Поведуй мне о себе через команду /pup_reg_people')
            #if(message.text[0:10].lower()=="меня зовут"):
                #with open(r"base/inf_people.txt", 'a', encoding='utf-8') as file:
                    #file.write(f"{message.from_user.id}:{(message.text)[11:]}\n")
                #bot.send_message(message.from_user.id, f"Приветствую,{(message.text)[11:]}!")


        

bot.polling(none_stop=True, interval=0)
