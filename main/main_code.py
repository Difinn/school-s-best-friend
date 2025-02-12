import telebot;
import random
import os
import sqlite3
import time
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

def get_sm(userid):
    with open(r"base/inf_people.txt", 'r', encoding='utf-8') as file:
        line = file.readline()        # считываем первую строку
        print(line, " ")

        while line != '':
            code = (line.split(":"))[0]  # пока не конец файла
            sm = (line.split(":"))[1]            
            if code == str(userid):      # обрабатываем считанную строку
                return sm

def change_sm(new_sm ,userid): #Это не робит
    linelist = []
    with open(r"base/inf_people.txt", 'r+', encoding='utf-8') as file:
        line = file.readline()        # считываем первую строку
        print(line, " ")

        while line != '':
            code = (line.split(":"))            # пока не конец файла
            if code == str(userid):      # обрабатываем считанную строку
                code[1] = new_sm
                linelist.append(":".join(code))
            else:
                linelist.append(line)
        
        with open("main.py", "w") as file:
            file.write(new_data)
            


bot = telebot.TeleBot(token = '7736265547:AAGnxKHv45qdeeWHlMqrWE_VzGPLCnfl0fw')


@bot.message_handler(commands = ['start'])
def send_welcome(message):                                    #стартовая команда
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


@bot.message_handler(commands = ["pup_reg_people"]) #регистрация людей
def pupi_reg_people(message):
    print((message.text).split())
    if(check_reg_people(message.from_user.id, message.chat.id)): #если есть в базе
        bot.send_message(message.from_user.id, 'Вы уже есть в базе')
    elif len((message.text).split())==4: #если есть 4 слова(команда + ФИО)
        print("Уяснил")
        name = (message.text).split() #я устал пиздец
        with open("base/inf_people.txt", 'a', encoding='utf-8') as file:
            file.write(f"{message.from_user.id}:1:{name[1]} {name[2]} {name[3]}\n") #Запист ФИО
        if not os.path.isdir(rf"base/inf_people/{message.from_user.id}"):
            os.mkdir(rf'base/inf_people/{message.from_user.id}')
    else:
        bot.send_message(message.from_user.id, 'Напиши свое Ф.И.О') #Стартер


@bot.message_handler(commands = ["pup_reg_group"])
def pupi_reg_group(message): #регистрация по аналогии с людьми
    number = message.chat.id
    if(check_reg_group(message.from_user.id, message.chat.id)):
        bot.send_message(message.chat.id, 'Уже в базе')
    else:
        with open(r"base/inf_groups.txt", 'a', encoding='utf-8') as file:
            file.write(f"{message.chat.id}:{message.text[15:]}")
        print(number)

        if not os.path.isdir(rf"base/inf_chats/{number}"):
            os.mkdir(rf'base/inf_chats/{number}')

        bot.send_message(message.chat.id, f'Привет, {number}!')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):

    seconds = time.time()           #настоящее время в секундах
    print(time.ctime(seconds))

    print(f"USER: {message.from_user.id}")
    print(f"CHAT:{message.chat.id}")
    
    if check_reg_people(message.from_user.id, message.chat.id): #проверки на запись в базе

        if check_reg_group(message.from_user.id, message.chat.id) or message.from_user.id==message.chat.id:

            
            #if check_reg_group(message.from_user.id, message.chat.id) and message.from_user.id != message.chat.id:
                #with open(rf"base/inf_chats/{message.chat.id}/", 'w+', encoding='utf-8') as file:
                    #file.write(f"{time.ctime(seconds)} {message.from_user.id}:{text.message}")

            # варианты

            #if(get_sm(message.from_user.id)=="1"):                                                             Это был тест на sm
                #bot.send_message(message.from_user.id, 'Вы зарегестироровались')
                #change_sm("2", message.from_user.id)
                

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
            if message.text == "10":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(types.KeyboardButton(text="Алгебра"))
                bot.send_message(message.chat.id, 'Выбери предмет!', reply_markup=markup)
            if message.text == "Алгебра":
                bot.send_document(message.chat.id, open(r'content/10/algebra/algebra-10-klass.pdf', 'rb'))

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
