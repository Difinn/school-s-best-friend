import telebot;
import random
import os
import sqlite3
import time
import schedule
from telebot import types

#есть id этого user в базе данных или нету(если есть, то true)
def check_reg_people(userid, chatid): #message.from_user.id and message.chat.id                  #есть id или нет
    db = sqlite3.connect("userstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[0] == userid:
            db.close()
            return True
    
    db.close()
    return False

#есть id этой группы в базе данных или нету(если есть, то true)
def check_reg_group(userid, chatid): #message.from_user.id and message.chat.id
    db = sqlite3.connect("groupstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[0] == userid:
            db.close()
            return True
    
    db.close()
    return False

#получаем на каком этапе(state macine) находится user
def get_sm(userid):
    db = sqlite3.connect("userstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[0] == userid:
            result = c[2]
    
    db.close()
    return result

#смена state macine
def change_sm(new_sm ,userid):
    db = sqlite3.connect("userstable.db")
    c = db.cursor()

    c.execute("UPDATE articles SET sm = new_sm WHERE id = userid")

#возвращает группы списком в которм есть пользователь
def get_groups(userid):
    db = sqlite3.connect("userstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[0] == userid:
            result = c[3].split(",")
    
    db.close()
    return result

#возвращает название группы из id
def get_groups_name_from_id(userid):
    db = sqlite3.connect("groupstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[0] == userid:
            result = c[1]
    
    db.close()
    return result

#возвращает id группы из имени
def get_groups_id_from_name(userid):
    db = sqlite3.connect("groupstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[1] == userid:
            result = c[0]
    
    db.close()
    return result


#возвращает участников группы по id в списке
def get_members(chatid):
    db = sqlite3.connect("groupstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[0] == chatid:
            result = c[2].split(",")
    
    db.close()
    return result

#из id ищет имя участника
def get_member_name_from_id(userid):
    db = sqlite3.connect("userstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[0] == userid:
            result = c[1]
    
    db.close()
    return result

#из имени ищет id
def get_member_id_from_name(userid):
    db = sqlite3.connect("userstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[0] == userid:
            result = c[1]
    
    db.close()
    return result

bot = telebot.TeleBot(token = '7736265547:AAGnxKHv45qdeeWHlMqrWE_VzGPLCnfl0fw')

#РАССЫЛКА МЕМОВ НАЧАЛО
def job():
    #тут для subscribed_users
    for user_id in subscribed_users:
        bot.send_message(chat_id=user_id, text="Это автоматическое сообщение.")

schedule.every().day.at("10:00").do(job)

while True:
    
    schedule.run_pending()
    time.sleep(1)
#РАССЫЛКА МЕМОВ ФИНАЛ


@bot.message_handler(commands = ['start'])
def send_welcome(message):                                    #стартовая команда
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text="Да! Помощь нужна."))
    markup.add(types.KeyboardButton(text="Нет!"))
    #print(message.chat.id, "Привет!", reply_markup = markup)
    # Получаем список групп, в которых находится бот
    #groups = bot.chat_ids

    # Записываем список групп в файл
    #with open("chats\base\inf_chats.txt", "w") as file:
        #file.write(str(groups))

    bot.send_message(message.chat.id, f"Привет! Тебе нужна помощь?", reply_markup = markup)


@bot.message_handler(commands = ["pup_reg_people"]) #регистрация людей
def pupi_reg_people(message):
    print((message.text).split())
    if(check_reg_people(message.from_user.id, message.chat.id)): #если есть в базе
        bot.send_message(message.from_user.id, 'Вы уже есть в базе в данных')
    elif len((message.text).split())==4: #если есть 4 слова(команда + ФИО)
        print("Запомнил")
        name = (message.text).split() #я устал пиздец
        with open("base/inf_people.txt", 'a', encoding='utf-8') as file:
            file.write(f"{message.from_user.id}:1:{name[1]} {name[2]} {name[3]}\n") #Запист ФИО
        if not os.path.isdir(rf"base/inf_people/{message.from_user.id}"):
            os.mkdir(rf'base/inf_people/{message.from_user.id}')
        change_sm("0:0", message.from_user.id)
    else:
        bot.send_message(message.from_user.id, 'Напиши свое Ф.И.О') #Стартер


@bot.message_handler(commands = ["pup_reg_group"])
def pupi_reg_group(message): #регистрация по аналогии с людьми
    number = message.chat.id
    if(check_reg_group(message.from_user.id, message.chat.id)):
        bot.send_message(message.chat.id, 'Уже есть в базе данных')
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

            #бекап и дз
            if check_reg_group(message.from_user.id, message.chat.id) and message.from_user.id != message.chat.id:
                if ((message.text).split("#"))[0] == "ДЗ":
                    pass

                else:
                    with open(rf"base/inf_chats/{message.chat.id}/", 'w+', encoding='utf-8') as file:
                        file.write(f"{time.ctime(seconds)} {message.from_user.id}:{message.text}")

            

            #if(get_sm(message.from_user.id)=="1"):                                                             Это был тест на sm
                #bot.send_message(message.from_user.id, 'Вы зарегестироровались')
                #change_sm("2", message.from_user.id)
            
            #if msg.text == "ЭБ, 1654356":  # Условые пересылки сообщения
                #bot.forward_message(
                #chat_id=1093110311,  # chat_id чата в которое необходимо переслать сообщение
                #from_chat_id=msg.chat.id,  # chat_id из которого необходимо переслать сообщение
                #message_id=msg.message_id  # message_id которое необходимо переслать
                #)
            
            # варианты    

            if message.text == "Да! Помощь нужна." or (get_sm(message.from_user.id).split(":"))[0] == "0":
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
                    change_sm("0:0", message.from_user.id)
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
                    change_sm("0:0", message.from_user.id)
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
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                pup_group = sorted(get_groups(message.from_user.id))
                mess = ""
                i = 1
                for c in pup_group:
                    markup.add(types.KeyboardButton(get_groups_name_from_id(c)))
                bot.send_message(message.chat.id, "Выбери нужную группу", reply_markup=markup)

                bot.register_next_step_handler(message, sm_group1)
                
            if (get_sm(message.from_user.id).split(":"))[0] == "pup_main":

                if message.text == "НАЗАД":
                    change_sm("0:0", message.from_user.id)
                
                #можешь сам решить как сделаешь. Но я предлагаю делать запись по типу #ДЗ#мат
                #мат улетает в базу и ты записываешь это с в таблу с id чата  из которого необходимо переслать сообщение и #message_id которое необходимо переслать
                elif message.text == "Д/З":
                    #if msg.text == "ЭБ, 1654356":  # Условые пересылки сообщения
                        #bot.forward_message(
                        #chat_id=1093110311,  # chat_id чата в которое необходимо переслать сообщение
                        #from_chat_id=msg.chat.id,  # chat_id из которого необходимо переслать сообщение
                        #message_id=msg.message_id  # message_id которое необходимо переслать
                        #)
                        pass
                
                elif message.text == "Список":
                    pup_list = sorted(get_members(message.chat.id))
                    mess = ""
                    i = 1
                    for c in pup_list:
                        mess += f"{str(i)}. {get_member_name_from_id(c)}\n"
                        i += 1
                    bot.send_message(message.chat.id, mess)
                
                #elif message.text == "Выбор отсутствующих":
                    #markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    #pup_list = sorted(get_members(message.chat.id))
                    #mess = ""
                    #i = 1
                    #for c in pup_list:
                        #markup.add(types.KeyboardButton(get_member_name_from_id(c)))
                    #bot.send_message(message.chat.id, "Выбери отсутствующего", reply_markup=markup)
                    #change_sm(f"absent:{(get_sm(message.from_user.id).split(':'))[1]}", message.from_user.id)
                    #bot.register_next_step_handler(message, set_absent1)
                    #Дальше смотри функцию set_absent1 ниже

                    #Но функцию забраковали :< Хотя можно сделать старосту
                
                #elif (get_sm(message.from_user.id).split(':'))[0] == "absent":
                    #userid = get_member_id_from_name(message.text)
                    #тут меняй на противоположное значение (по базе ученик присутствует(1))
                    #change_sm("pup_main", message.from_user.id)
                else:
                    change_sm("pup_main", message.from_user.id)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(types.KeyboardButton(text="Д/З"))
                    markup.add(types.KeyboardButton(text="Список"))
                    markup.add(types.KeyboardButton(text="Мероприятия"))
                    #markup.add(types.KeyboardButton(text="Выбор отсутствующих"))
                    #markup.add(types.KeyboardButton(text="Игры"))
                    markup.add(types.KeyboardButton(text="НАЗАД"))
                    bot.send_message(message.chat.id, 'Выбери опцию', reply_markup=markup)
            
            #учитель
            if message.text == "УЧИТЕЛЬ":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                pup_group = sorted(get_groups(message.from_user.id))
                mess = ""
                i = 1
                for c in pup_group:
                    markup.add(types.KeyboardButton(get_groups_name_from_id(c)))
                bot.send_message(message.chat.id, "Выбери нужную группу", reply_markup=markup)
                
            if (get_sm(message.from_user.id).split(":"))[0] == "teach_main":
                if message.text == "НАЗАД":
                    change_sm("0:0", message.from_user.id)
                
                #Это функция сделана и ее трогать не надо!!!
                elif message.text == "Список":
                    pup_list = sorted(get_members(message.chat.id))
                    mess = ""
                    i = 1
                    for c in pup_list:
                        mess += f"{str(i)}. {get_member_name_from_id(c)}\n"
                        i += 1
                    bot.send_message(message.chat.id, mess)
                
                #Это График и его НАДО СДЕЛАТЬ
                elif message.text == "График посещаемости ученика":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    pup_list = sorted(get_members(message.chat.id))
                    mess = ""
                    for c in pup_list:
                        markup.add(types.KeyboardButton(get_member_name_from_id(c)))
                    bot.send_message(message.chat.id, "Выбери ученика для проверки", reply_markup=markup)

                    change_sm(f"graf:{(get_sm(message.from_user.id).split(':'))[1]}", message.from_user.id)
                    bot.register_next_step_handler(message, send_graf)
                
                elif message.text == "Мероприятия":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(types.KeyboardButton(text="Создать"))
                    markup.add(types.KeyboardButton(text="Посмотреть"))
                    markup.add(types.KeyboardButton(text="Руководство"))
                    bot.send_message(message.chat.id, 'Выбери опцию', reply_markup=markup)

                    change_sm(f"party:{(get_sm(message.from_user.id).split(':'))[1]}", message.from_user.id)

                    bot.register_next_step_handler(message, party)
                

                elif message.text == "Выбор отсутствующих":
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    pup_list = sorted(get_members(message.chat.id))
                    mess = ""
                    i = 1
                    for c in pup_list:
                        markup.add(types.KeyboardButton(get_member_name_from_id(c)))
                    bot.send_message(message.chat.id, "Выбери отсутствующего", reply_markup=markup)

                    change_sm(f"absent:{(get_sm(message.from_user.id).split(':'))[1]}", message.from_user.id)
                    bot.register_next_step_handler(message, set_absent2)
                    #Дальше смотри функцию set_absent2 ниже

                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    markup.add(types.KeyboardButton(text="Список"))
                    markup.add(types.KeyboardButton(text="Мероприятия"))
                    markup.add(types.KeyboardButton(text="График посещаемости ученика"))
                    markup.add(types.KeyboardButton(text="Выбор отсутствующих"))
                    markup.add(types.KeyboardButton(text="НАЗАД"))
                    #markup.add(types.KeyboardButton(text="Игры"))
                    bot.send_message(message.chat.id, 'Выбери опцию', reply_markup=markup)

                
        else:
            bot.send_message(message.chat.id, 'Зарегистрируйте /pup_reg_group')


    else:
        bot.send_message(message.from_user.id, 'Поведуй мне о себе через команду /pup_reg_people')

def set_absent1(message):
    if (get_sm(message.from_user.id).split(":"))[0] == "absent":
        userid = get_member_id_from_name(message.text)
        #тут меняй на противоположное значение (по базе ученик присутствует(1))
        change_sm(f"pup_main:{(get_sm(message.from_user.id).split(':'))[1]}", message.from_user.id)

def set_absent2(message):
    if (get_sm(message.from_user.id).split(":"))[0] == "absent":
        userid = get_member_id_from_name(message.text)

        bot.send_message(userid, 'Вас обозначали, как отсутсвующего.')

        #тут меняй на противоположное значение (по базе ученик присутствует(1))

        change_sm(f"teach_main:{(get_sm(message.from_user.id).split(':'))[0]}", message.from_user.id)

def send_graf(message):
    if (get_sm(message.from_user.id).split(":"))[0] == "graf":
    #дальше сам делаешь
        pass
    change_sm(f"teach_main:{(get_sm(message.from_user.id).split(':'))[1]}", message.from_user.id)

#это смотреть надо, как работает (это для ученика)
def sm_group1(message):
    change_sm(f"pup_main:{get_groups_id_from_name(message.text)}", message.from_user.id)
    bot.send_message(message.chat.id, "Принято")

#это смотреть надо, как работает (это для учителя)
def sm_group2(message):
    change_sm(f"teach_main:{get_groups_id_from_name(message.text)}", message.from_user.id)
    bot.send_message(message.from_user.id, "Дайте название данному событию.")

def party(message):
    if message.text == "Создать":
        bot.send_message(message.chat.id, "Принято")
        bot.register_next_step_handler(message, party_name)
    elif message.text == "Посмотреть":
        pass
    elif message.text == "Руководство":
        pass

def party_name(message):
    #Тут сделай запись в табличку, наверное
    bot.register_next_step_handler(message, party_description)

def party_description(message):
    #Тут сделай запись в табличку, наверное
    bot.send_message(message.chat.id, "Принято. Введите описание события.")
    bot.register_next_step_handler(message, party_time)

def party_time(message):
    #Тут сделай запись в табличку, наверное
    bot.send_message(message.chat.id, "Мероприятие создано")




bot.polling(none_stop=True, interval=0)