import telebot;
import random
import os
import sqlite3
import time
from telebot import types

#есть id этого user в базе данных или нету(если есть, то true)
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

#есть id этой группы в базе данных или нету(если есть, то true)
def check_reg_group(userid, chatid): #message.from_user.id and message.chat.id
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

#получаем на каком этапе(state macine) находится user
def get_sm(userid):
    with open(r"base/inf_people.txt", 'r', encoding='utf-8') as file:
        line = file.readline()        # считываем первую строку
        print(line, " ")

        while line != '':
            code = (line.split(":"))[0]  # пока не конец файла
            sm = (line.split(":"))[1]            
            if code == str(userid):      # обрабатываем считанную строку
                return sm

#смена state macine
def change_sm(new_sm ,userid):
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

#возвращает группы списком
def get_groups(userid):
    pass

#возвращает участников группы по id в списке
def get_members(chatid):
    pass

#из id ищет имя участника
def get_member_name_from_id(userid):
    pass

#из имени ищет id
def get_member_id_from_name(userid):
    pass

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
        change_sm("0", message.from_user.id)
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

    seconds = time.time()
    #настоящее время в секундах           
    print(time.ctime(seconds))

    print(f"USER: {message.from_user.id}")
    print(f"CHAT:{message.chat.id}")
    
    #проверки на запись в базе
    if check_reg_people(message.from_user.id, message.chat.id): 

        if check_reg_group(message.from_user.id, message.chat.id) or message.from_user.id==message.chat.id:

            
            #if check_reg_group(message.from_user.id, message.chat.id) and message.from_user.id != message.chat.id:
                #with open(rf"base/inf_chats/{message.chat.id}/", 'w+', encoding='utf-8') as file:
                    #file.write(f"{time.ctime(seconds)} {message.from_user.id}:{text.message}")

            

            #if(get_sm(message.from_user.id)=="1"):                                                             Это был тест на sm
                #bot.send_message(message.from_user.id, 'Вы зарегестироровались')
                #change_sm("2", message.from_user.id)
            
            # варианты    

            if message.text == "ДА! Помощь нужна." or get_sm(message.from_user.id) == "0":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True) #создание новых кнопок
                btn1 = types.KeyboardButton('УЧЕНИК')
                btn2 = types.KeyboardButton('УЧИТЕЛЬ')
                btn3 = types.KeyboardButton('БИБЛИОТЕКА')
                markup.add(btn1, btn2, btn3)
                bot.send_message(message.chat.id, 'Выбирай, путник!', reply_markup=markup)
            
            if message.text == "БИБЛИОТЕКА":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                #markup.add(types.KeyboardButton(text="8")) Мне в падлу искать учебники для 8 :3
                markup.add(types.KeyboardButton(text="9"))
                markup.add(types.KeyboardButton(text="10"))
                markup.add(types.KeyboardButton(text="НАЗАД"))
                bot.send_message(message.chat.id, 'Из какого ты класса?', reply_markup=markup)
            
            #Библиотека за 10 класс
            if message.text == "10" or get_sm(message.from_user.id)=="lib_10":
                change_sm("lib_10", message.from_user.id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(types.KeyboardButton(text="Алгебра"))
                markup.add(types.KeyboardButton(text="История"))
                markup.add(types.KeyboardButton(text="Английский"))
                bot.send_message(message.chat.id, 'Выбери предмет!', reply_markup=markup)
            
            
            if get_sm(message.from_user.id) == "lib_10":
                if message.text == "НАЗАД":
                    change_sm("0", message.from_user.id)
                if message.text == "Алгебра":
                    bot.send_document(message.chat.id, open(r'content/10/algebra/10_algebra.pdf', 'rb'))
                    change_sm("lib_10", message.from_user.id)
                if message.text == "Английский":
                    bot.send_document(message.chat.id, open(r'content/10/english/10_spotlight.pdf', 'rb'))
                    change_sm("lib_10", message.from_user.id)
                if message.text == "История":
                    bot.send_document(message.chat.id, open(r'content/10/history/10_history.pdf', 'rb'))
                    change_sm("lib_10", message.from_user.id)
            
            #Библиотека за 9 класс
            if message.text == "9" or get_sm(message.from_user.id)=="lib_9":
                change_sm("lib_9", message.from_user.id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(types.KeyboardButton(text="Алгебра"))
                markup.add(types.KeyboardButton(text="История"))
                markup.add(types.KeyboardButton(text="Английский"))
                bot.send_message(message.chat.id, 'Выбери предмет!', reply_markup=markup)
            if get_sm(message.from_user.id) == "lib_9":
                if message.text == "НАЗАД":
                    change_sm("0", message.from_user.id)
                if message.text == "Алгебра":
                    bot.send_document(message.chat.id, open(r'content/10/algebra/10_algebra.pdf', 'rb'))
                    change_sm("lib_9", message.from_user.id)
                if message.text == "Английский":
                    bot.szend_document(message.chat.id, open(r'content/10/english/10_spotlight.pdf', 'rb'))
                    change_sm("lib_9", message.from_user.id)
                if message.text == "История":
                    bot.send_document(message.chat.id, open(r'content/10/history/10_history.pdf', 'rb'))
                    change_sm("lib_9", message.from_user.id)

            #ученик
            if message.text == "УЧЕНИК":
                change_sm("pup_main", message.from_user.id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(types.KeyboardButton(text="Д/З"))
                markup.add(types.KeyboardButton(text="Список"))
                markup.add(types.KeyboardButton(text="Выбор отсутствующих"))
                #markup.add(types.KeyboardButton(text="Игры"))
                markup.add(types.KeyboardButton(text="НАЗАД"))
                bot.send_message(message.chat.id, 'Выбери опцию', reply_markup=markup)
            
            if get_sm(message.from_user.id) == "pup_main":
                if message.text == "НАЗАД":
                    change_sm("0", message.from_user.id)
                
                if message.text == "Список":
                    pup_list = sorted(get_members(message.chat.id))
                    mess = ""
                    i = 1
                    for c in list:
                        mess += f"{str(i)}. {get_member_name_from_id(c)}\n"
                        i += 1
                    bot.send_message(message.chat.id, mess)

                    change_sm("teach_main", message.from_user.id)
                
                if message.text == "Выбор отсутствующих":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    pup_list = sorted(get_members(message.chat.id))
                    mess = ""
                    i = 1
                    for c in list:
                        markup.add(types.KeyboardButton(get_member_name_from_id(c)))
                    bot.send_message(message.chat.id, "Выбери отсутствующего", reply_markup=markup)

                    change_sm("absent", message.from_user.id)
                    bot.register_next_step_handler(message, set_absent1)
                    #Дальше смотри функцию set_absent1 ниже
                
                if get_sm(message.from_user.id) == "absent":
                    userid = get_member_id_from_name(message.text)
                    #тут меняй на противоположное значение (по базе ученик присутствует(1))
                    change_sm("pup_main", message.from_user.id)
            
            #учитель
            if message.text == "УЧИТЕЛЬ":

                change_sm("teach_main", message.from_user.id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                markup.add(types.KeyboardButton(text="Список"))
                markup.add(types.KeyboardButton(text="График посещаемости ученика"))
                markup.add(types.KeyboardButton(text="Выбор отсутствующих"))
                markup.add(types.KeyboardButton(text="НАЗАД"))
                #markup.add(types.KeyboardButton(text="Игры"))
                bot.send_message(message.chat.id, 'Выбери опцию', reply_markup=markup)
            if get_sm(message.from_user.id) == "teach_main":
                if message.text == "НАЗАД":
                    change_sm("0", message.from_user.id)
                
                if message.text == "Список":
                    pup_list = sorted(get_members(message.chat.id))
                    mess = ""
                    i = 1
                    for c in list:
                        mess += f"{str(i)}. {get_member_name_from_id(c)}\n"
                        i += 1
                    bot.send_message(message.chat.id, mess)

                    change_sm("teach_main", message.from_user.id)
                
                if message.text == "Выбор отсутствующих":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    pup_list = sorted(get_members(message.chat.id))
                    mess = ""
                    i = 1
                    for c in list:
                        markup.add(types.KeyboardButton(get_member_name_from_id(c)))
                    bot.send_message(message.chat.id, "Выбери отсутствующего", reply_markup=markup)

                    change_sm("absent", message.from_user.id)
                    bot.register_next_step_handler(message, set_absent2)
                    #Дальше смотри функцию set_absent2 ниже
                
        else:
            bot.send_message(message.chat.id, 'Зарегистрируйте /pup_reg_group')


    else:
        bot.send_message(message.from_user.id, 'Поведуй мне о себе через команду /pup_reg_people')

def set_absent1(message):
    if get_sm(message.from_user.id) == "absent":
        userid = get_member_id_from_name(message.text)
        #тут меняй на противоположное значение (по базе ученик присутствует(1))
        change_sm("pup_main", message.from_user.id)

def set_absent2(message):
    if get_sm(message.from_user.id) == "absent":
        userid = get_member_id_from_name(message.text)
        #тут меняй на противоположное значение (по базе ученик присутствует(1))
        change_sm("teach_main", message.from_user.id)


        

bot.polling(none_stop=True, interval=0)
