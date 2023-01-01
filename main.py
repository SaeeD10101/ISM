#main commands and bot creation

import json
import telebot
from telebot import types,util
from decouple import config
from googletrans import Translator
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
 
BOT_TOKEN = config('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)
bot_data={
"names":["ISM","BOT"]

}
text_messages={
    "welcome":"welcome to Saeed bot just a bot to manage your group",
    "welcomeNewMember":
                      u"اهلا بك {name} في مجموعتنا الخاصه",
    "godbay":
    u"العضو{name} غادر المجموعة",
    "botname":
    "كيف يمكنني مساعدتك ؟",
    "warn":
    u"لقد استعمل {name} الكلمات المحضوره\n"
    u"  سيتم طردك بعد{safeCounter} من المحاولات ",
    "kicked":u"👮‍♂️⚠ لقد تم طرد العضو {name} صاحب المعرف {username} بسبب مخالفته لاحد قواعد المجموعة 👮‍♂️⚠",
    "file":u"ملف!",
    "photo":u"صورة!"

                    
    

}
text_list={
"offensive":["rat","dog"]

}

commands ={
"Translate":["translate","trans","Translate","ترجم"]

} 
def handleNewUserData(message):
    id = str(message.new_chat_member.user.id)
    name = message.new_chat_member.user.first_name
    username =  message.new_chat_member.user.username

    with open("data.json","r") as jsonFile:
        data = json.load(jsonFile)
    jsonFile.close()
    users = data["users"]
    if id not in users:
        print("new user detected !")
        users[id] = {"safeCounter":5}
        users[id]["username"] = username
        users[id]["name"] = name
        print("new user data saved !")

    data["users"] = users
    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()  
def handleOffensiveMessage(message):
 id = str(message.from_user.id)
 name = message.from_user.first_name
 username = message.from_user.username

 with open ("data.json") as jsonfile:
    data=json.load(jsonfile)
    jsonfile.close()
    users = data["users"]
    if id not in users:
       
        users[id]= {"safeCounter":5}
        users[id]["username"]= username
        users[id]["name"]= name

    for index in users:
        if index == id:
            print("guilty user founded !")
            users[id]["safeCounter"] -=1
   
 safeCounterFromJson = users[id]["safeCounter"]
 if safeCounterFromJson == 0:
    bot.kick_chat_member(message.chat.id,id)
    users.pop(id)
    bot.send_message(message.chat.id,text_messages["kicked"].format(name=name , username=username))
 else:
    bot.send_message(message.chat.id,text_messages["warn"].format(name=name, safeCounter = safeCounterFromJson))
    data["users"]= users

    with open("data.json","w") as editedFile:
        json.dump(data,editedFile,indent=3)
    editedFile.close()
 return bot.delete_message(message.chat.id,message.message_id)
@bot.message_handler(commands=["start","help"])
def start(message):
    bot.send_message(message.chat.id,text_messages["welcome"])

#saying welcome to the new members
#saying godbay to left members
@bot.chat_member_handler()
def handleUserUpdates(message:types.ChatMemberUpdated):
    newResponse = message.new_chat_member
    if newResponse.status == "member":
       handleNewUserData(message=message)
       bot.send_message(message.chat.id,text_messages['welcomeNewMember'].format(name=newResponse.user.first_name))
    if newResponse.status=="left":
        bot.send_message(message.chat.id,text_messages['godbay'].format(name=newResponse.user.first_name))
 
#Listening to the group messages 
@bot.message_handler(func=lambda m:True)
def replay(message):
    words = message.text.split()
    if words [0] in bot_data['names']:
       bot.reply_to(message,text_messages['botname']) 
    if words [0] in commands["Translate"]:
        translator = Translator()
        translation = translator.translate(" ".join(words[1:]),dest="ar")
        bot.reply_to(message,translation.text)
    if words [0] in text_messages["file"]:
         bot.send_document(message.chat.id,open('ca.pdf','rb'))
    if words [0] in text_messages["photo"]:
         bot.send_photo(message.chat.id,open('111.jpg','rb'))
    for word in words :
        if word in text_list["offensive"]:
         handleOffensiveMessage(message=message)
    
        
bot.infinity_polling(allowed_updates=util.update_types)
