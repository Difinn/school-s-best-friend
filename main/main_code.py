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
        if c[0] == str(userid):
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
        if c[0] == str(userid):
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
        if c[0] == str(userid):
            result = c[2]
    
    db.close()
    return result

#смена state macine
def change_sm(new_sm ,userid):
    db = sqlite3.connect("userstable.db")
    c = db.cursor()
    userid = str(userid)

    c.execute("UPDATE articles SET sm = ? WHERE id = ?", (new_sm, userid))
    db.commit()  # Важно!
    db.close()

#возвращает группы списком в которм есть пользователь
def get_groups(userid):
    db = sqlite3.connect("userstable.db")
    c = db.cursor()
    c.execute("SELECT groups FROM articles WHERE id = ?", (str(userid),))       # посмотри на запятую

    all = c.fetchall()
    result = (all[0][0]).split(",")

    return result

#возвращает название группы из id
def get_groups_name_from_id(userid):
    db = sqlite3.connect("groupstable.db")
    c = db.cursor()
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    result = "0"
    for c in all:
        if c[0] == str(userid):
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
        if c[1] == str(userid):
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
        if c[0] == str(chatid):
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
        if c[0] == str(userid):
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
        if c[0] == str(userid):
            result = c[1]
    
    db.close()
    return result

def get_event_inf(idishnik):
    db = sqlite3.connect("eventstable.db")
    c = db.cursor()
    idishnik = int(idishnik)
    c.execute("SELECT rowid, * FROM articles WHERE rowid = ?", (idishnik))

    all = c.fetchall()

    db.commit()
    db.close()
    return all[0]

def check_member_in_group(userid, chatid):
    #db = sqlite3.connect("userstable.db")
    #c = db.cursor()

    dbg = sqlite3.connect("groupstable.db")
    cg = db.cursor()
    
    cg = ("SELECT participants FROM articles WHERE id = ?", (str(chatid)))
    all = cg.fetchall()

    party = all[0].split(",")

    if userid not in party:
        dbg.commit()
        dbg.close()
        return True
    
    dbg.commit()
    dbg.close()    
    return False


bot = telebot.TeleBot(token = '7575924161:AAHw3OG5W9R3sCUwc-Yrdh3-JfCU5srMrFk')

#РАССЫЛКА МЕМОВ НАЧАЛО
#def job():
    #тут для subscribed_users
    #for user_id in subscribed_users:
        #bot.send_message(chat_id=user_id, text="Это автоматическое сообщение.")

#schedule.every().day.at("10:00").do(job)

#while True:
    
    #schedule.run_pending()
    #time.sleep(1)
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
    else:
        bot.send_message(message.from_user.id, 'Напишите ваше ФИО.')
        bot.register_next_step_handler(message, reg_name)

def reg_name(message):
    name = message.text

    bot.send_message(message.from_user.id, 'Напишите вашу Роль')
    bot.register_next_step_handler(message, reg_role, name)

def reg_role(message, name):
    role = message.text

    bot.send_message(message.from_user.id, 'Когда вы родились?')
    bot.register_next_step_handler(message, reg_birth, name, role)

def reg_birth(message, name, role):
    birth = message.text
    id = message.from_user.id

    m_time = message.text

    
    db = sqlite3.connect("userstable.db")
    c = db.cursor()

    #c.execute("INSERT INTO articles VALUES (id, name, '0:0', '', birth, role)")
    c.execute("""
    INSERT INTO articles (id, name, sm, groups, birth_date, role)
    VALUES (?, ?, ?, ?, ?, ?)
""", (id, name, '0:0', '', birth, role))
    
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    print(all)
    db.commit()
    db.close()

    bot.send_message(message.from_user.id, f'Поздравляю, {name}! Вы зарегестрировались.')

        


@bot.message_handler(commands = ["pup_reg_group"])
def pupi_reg_group(message): #регистрация по аналогии с людьми
    number = message.chat.id
    if(check_reg_group(message.from_user.id, message.chat.id)):
        bot.send_message(message.chat.id, 'Уже есть в базе данных')
    elif (check_reg_group(message.from_user.id, message.chat.id)) == False and (str(message.from_user.id) != str(message.chat.id)):
        bot.send_message(message.chat.id, 'Какое название у группы?')
        bot.register_next_step_handler(message, reg_nameg)

def reg_nameg(message):
    name = message.text
    id = message.chat.id
    
    db = sqlite3.connect("userstable.db")
    c = db.cursor()

    #c.execute("INSERT INTO articles VALUES (id, name, '0:0', '', birth, role)")
    c.execute("""
    INSERT INTO articles (id, name, participants, otchim, events)
    VALUES (?, ?, ?, ?, ?)
    """, (id, name, str(message.from_user.id), str(message.from_user.id), ''))
    
    c.execute("SELECT * FROM articles")

    all = c.fetchall()
    print(all)
    db.commit()
    db.close()

    bot.send_message(message.chat.id, f'Удачного пользования!')


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
                
                if check_member_in_group(message.from_user.id, message.chat.id):
                    db = sqlite3.connect("userstable.db")
                    c = db.cursor()

                    dbg = sqlite3.connect("groupstable.db")
                    cg = db.cursor()
                    
                    cg = ("SELECT participants FROM articles WHERE id = ?", (str(message.chat.id)))
                    all = cg.fetchall()
                    party = all[0] + "," + str(message.from_user.id)
                    cg = ("UPDATE articles SET participants = ? WHERE id = ?", (party, str(message.chat.id)))

                    c = ("SELECT groups FROM articles WHERE id = ?", (str(message.chat.id)))
                    allc = c.fetchall()
                    groups = all[0] + "," + str(message.chat.id)
                    c = ("UPDATE articles SET groups = ? WHERE id = ?", (groups, str(message.chat.id)))

                    db.commit()
                    db.close()

                    dbg.commit()
                    dbg.close()


            

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
                    bot.send_document(message.chat.id, open(r'content/10/english/10_spotlight.pdf', 'rb'))
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
        bot.send_message(message.chat.id, "Принято. Введите имя события.")
        bot.register_next_step_handler(message, party_name)
    elif message.text == "Посмотреть":
        db = sqlite3.connect("groupstable.db")


        c = db.cursor()

        group = (get_sm(message.from_user.id).split(":"))[0]
        c.execute("SELECT events FROM articles WHERE id = ?", (group))
        events = c.fetchall()
        
        for hah in events:
            markup.add(types.KeyboardButton((get_event_inf(hah))[1]))

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.chat.id, 'Выберите событие', reply_markup=markup)

        db.commit()
        db.close()

        bot.register_next_step_handler(message, party_inf, events)
        
    elif message.text == "Руководство":
        pass

def party_name(message):
    name = message.text

    bot.send_message(message.chat.id, "Принято. Введите описание события.")
    #Тут сделай запись в табличку, наверное
    bot.register_next_step_handler(message, party_description, name)

def party_description(message, name):
    desc = message.text

    #Тут сделай запись в табличку, наверное
    bot.send_message(message.chat.id, "Принято. Введите время события.")
    bot.register_next_step_handler(message, party_time, name, desc)

def party_time(message, name, desc):
    time = message.text

    #Тут сделай запись в табличку, наверное
    bot.send_message(message.chat.id, "Принято. Когда напомнить о событии?")
    bot.register_next_step_handler(message, m_party_time, name, desc, time)
def m_party_time(message, name, desc, time):
    m_time = message.text

    
    db = sqlite3.connect("eventstable.db")
    db_g = sqlite3.connect("groupstable.db")
    c = db.cursor()
    c_g = db_g.cursor()

    c.execute("INSERT INTO articles (name, description, time, notifications) VALUES (?, ?, ?, ?)", (name, desc, time, m_time))
    c.execute("SELECT rowid FROM articles")

    a = len(c.fetchall())
    idishnik = (get_sm(message.from_user.id).split(":"))[1]

    c_g.execute("SELECT events, participants FROM articles WHERE id = ?", (idishnik))
    new_event = (c_g.fetchall())[0][0] + ","+ str(a)

    for c in (c_g.fetchall())[0][1]:
        bot.send_message(c, f"Новое событие '{name}':\n{desc}")
        #этот моментик проверить надо

    c_g.execute("UPDATE articles SET event = ? WHERE id = ?", (new_event, idishnik))

    db.commit()
    db.close()
    db_g.commit()
    db_g.close()

    


    bot.send_message(message.chat.id, "Событие создано")

def party_inf(message, events):
    for c in events:
        if message == c[2]:
            bot.send_message(c, f"Новое событие '{c[2]}':\n{c[3]}")






bot.polling(none_stop=True, interval=0)