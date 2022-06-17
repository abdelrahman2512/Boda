import os
import time
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re
import datetime
import redis
from utils.config import token,bot_id,sudo
from utils.func import app,channel_id,motors,bot,admins,manager,sudos,channel


data = redis.Redis("127.0.0.1",6379)

def del_c(client,message):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)
    text = str(message.text)
    message_id = str(message.message_id)
    if str(message.chat.type) in ['group','supergroup']:
        if text == "تفعيل التلقائي" or text == "تفعيل المسح التلقائي":
            if channel(user_id):
                if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
                    if manager(chat_id,user_id):
                        data.set(bot_id+"mediapy-time-"+str(message.chat.id),str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute))
                        bot("sendMessage",{"chat_id":chat_id,"text":"*تم تفعيل المسح التلقائي \nلتعيين عدد المسح ارسل :- عدد المسح*","reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                        data.sadd(bot_id+"-mediapy-auto",str(chat_id))
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})

        if text == "تعطيل التلقائي" or text == "تعطيل المسح التلقائي":
            if channel(user_id):
                if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
                    if manager(chat_id,user_id):
                        bot("sendMessage",{"chat_id":chat_id,"text":"*تم تعطيل المسح التلقائي*","reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                        data.srem(bot_id+"-mediapy-auto",str(chat_id))
                        data.delete(bot_id+"mediapy-time-"+str(message.chat.id))
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})

        if text == "عدد المسح" or text == "تعين عدد المسح" or text == "تعيين عدد المسح":
            if channel(user_id):
                if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
                    if manager(chat_id,user_id):
                        bot("sendMessage",{"chat_id":chat_id,"text":"حسنا عزيزي الان ارسل العدد بالارقام الانجليزية","reply_to_message_id":message_id})
                        data.set(bot_id+"-auto-lmsgs-wait"+chat_id,f"{user_id}")

            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})

        if text == "مسح عدد المسح" or text == "حذف عدد المسح":
            if channel(user_id):
                if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
                    if manager(chat_id,user_id):
                        bot("sendMessage",{"chat_id":chat_id,"text":"تم حذف عدد المسح بنجاح","reply_to_message_id":message_id})
                        data.delete(bot_id+"-auto-cmsgs-"+chat_id)
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})

        if re.match("^عدد المسح \d+$",str(text)):
            if channel(user_id):
                if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
                    if manager(chat_id,user_id):
                        st = text.split(sep=" ")[2]
                        full = range(1,100000)
                        try:
                            if int(st) in full:
                                data.set(bot_id+"-auto-cmsgs-"+chat_id,str(st))
                                bot("sendMessage",{"chat_id":chat_id,"text":"تم حفظ عدد المسح بنجاح","reply_to_message_id":message_id})
                            elif int(st) == 0:
                                bot("sendMessage",{"chat_id":chat_id,"text":"عذرا لا يمكن حفظ الصفر ! \n اعد المحاوله وارسل عدد اخر اصغر من 100000","reply_to_message_id":message_id})
                            else:
                                bot("sendMessage",{"chat_id":chat_id,"text":"العدد كبير جدا ! \n اعد المحاوله وارسل عدد اقل من 100000","reply_to_message_id":message_id})
                        except Exception:
                            bot("sendMessage",{"chat_id":chat_id,"text":"ارسل الرقم باللغه الانجليزيه رجاءا !","reply_to_message_id":message_id})
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})

        if data.get(bot_id+"-auto-lmsgs-wait"+chat_id):
            if str(data.get(bot_id+"-auto-lmsgs-wait"+chat_id).decode()) == user_id:
                full = range(1,100000)
                try:
                    if int(text) in full:
                        data.set(bot_id+"-auto-cmsgs-"+chat_id,str(text))
                        bot("sendMessage",{"chat_id":chat_id,"text":"تم حفظ عدد المسح بنجاح","reply_to_message_id":message_id})
                    elif int(text) == 0:
                        bot("sendMessage",{"chat_id":chat_id,"text":"عذرا لا يمكن حفظ الصفر ! \n اعد المحاوله وارسل عدد اخر اصغر من 100000","reply_to_message_id":message_id})
                    else:
                        bot("sendMessage",{"chat_id":chat_id,"text":"العدد كبير جدا ! \n اعد المحاوله وارسل عدد اقل من 100000","reply_to_message_id":message_id})
                except Exception:
                    bot("sendMessage",{"chat_id":chat_id,"text":"ارسل الرقم باللغه الانجليزيه رجاءا !","reply_to_message_id":message_id})
                finally:
                    data.delete(bot_id+"-auto-lmsgs-wait"+chat_id)

def broad(client,message):
    if str(message.from_user.id) == str(sudo):
        if data.get(bot_id+"-mediapy-wait"):
            if data.get(bot_id+"-mediapy-wait").decode() == "broad":
                try:
                    chats = data.sinter(bot_id+"-mediapy-chats") if data.sinter(bot_id+"-mediapy-chats") else None
                    if chats != None:
                        for i in chats:
                            res = bot("sendMessage",{"chat_id":i.decode(),"text":message.text,"parse_mode":"MarkDown"})
                            data.srem(bot_id+"-mediapy-chats",i.decode()) if res["ok"] != True else print(True)
                except Exception:
                    chats = None
                try:
                    members = data.sinter(bot_id+"-mediapy-members") if data.sinter(bot_id+"-mediapy-chats") else None
                    if members != None:
                        for i in members:
                            res = bot("sendMessage",{"chat_id":i.decode(),"text":message.text})
                            data.srem(bot_id+"-mediapy-members",i.decode()) if res["ok"] != True else print(True)
                except Exception:
                    members = None
                os.system("service redis restart")
                os.system("service redis-server restart")
                os.system("service redis start")
                os.system("service redis-server start")
                try:
                    c_chats = len(data.sinter(bot_id+"-mediapy-chats")) if data.sinter(bot_id+"-mediapy-chats") else 0
                except Exception:
                    c_chats = 0
                try:
                    c_members = len(data.sinter(bot_id+"-mediapy-members"))-1 if data.sinter(bot_id+"-mediapy-chats") else 0
                except Exception:
                    c_members = 0
                cmembers = str(c_chats+c_members)
                bot("sendMessage",{"chat_id":sudo,"text":"تمت الاذاعه الى {} من المجموعات والمشتركين".format(cmembers)})
                data.delete(bot_id+"-mediapy-wait")

def c_count(client,message):
    chat_id = message.chat.id
    message_id = message.message_id
    text = message.text
    user_id = message.from_user.id
    if text == "الاحصائيات":
        if motors(user_id):
            groups = len(data.sinter(bot_id+"-mediapy-chats")) if data.sinter(bot_id+"-mediapy-chats") else 0
            members = len(data.sinter(bot_id+"-mediapy-members"))-1 if data.sinter(bot_id+"-mediapy-members") else 0
            txt = f"عدد المجموعات :- {str(groups)}\nعدد المشتركين :- {str(members)}\nالعدد الكلي :- {str(groups+members)}"
            app.send_message(chat_id,text=txt,reply_to_message_id=message_id)

def s_channel(client,message):
    chat_id = message.chat.id
    message_id = message.message_id
    text = message.text
    user_id = message.from_user.id
    if text:
        if str(user_id) == str(sudo):
            if text in ['تعيين قناة الاشتراك الاجباري',"تعين قناة الاشتراك الاجباري"]:
                data.delete(bot_id+"-mediapy-channel")
                data.set(bot_id+"-mediapy-wait","channel")
                app.send_message(chat_id=chat_id,text="حسنا عزيزي ارسل الان معرف او ايدي القناة وتاكد من رفع البوت مشرف في القناة",reply_to_message_id=message_id)
            else:
                if data.get(bot_id+"-mediapy-wait"):
                    if data.get(bot_id+"-mediapy-wait").decode() == "channel":
                        data.delete(bot_id+"-mediapy-channel")
                        if re.match("^-100\d{10}$",message.text):
                            data.set(bot_id+"-mediapy-channel",str(message.text))
                            txt = "تم حفظ قناة الاشتراك الاجباري بنجاح"
                        elif re.match("^\d{10}$",message.text):
                            data.set(bot_id+"-mediapy-channel","-100"+str(message.text))
                            txt = "تم حفظ قناة الاشتراك الاجباري بنجاح"
                        elif re.match("^@(.*)$",message.text) and not re.match("\s",str(message.text)):
                            ge = app.get_chat(message.text)
                            if ge.id:
                                data.set(bot_id+"-mediapy-channel",str(ge.id))
                                txt = "تم حفظ قناة الاشتراك الاجباري بنجاح"
                            else:
                                txt = "المعرف خاطئ اعد ارسال الامر ( تعيين قناة الاشتراك الاجباري ) ثم ارسل معرف صحيح"
                        else:
                            ge = app.get_chat(message.text)
                            if ge.id:
                                data.set(bot_id+"-mediapy-channel",str(ge.id))
                                txt = "تم حفظ قناة الاشتراك الاجباري بنجاح"
                            else:
                                txt = "المعرف خاطئ اعد ارسال الامر ( تعيين قناة الاشتراك الاجباري ) ثم ارسل معرف صحيح"
                        app.send_message(chat_id=chat_id,text=txt,reply_to_message_id=message_id)
                        data.delete(bot_id+"-mediapy-wait")
                        os.system("service redis restart")
                        os.system("service redis-server restart")
                        os.system("service redis start")
                        os.system("service redis-server start")
                        exit()
            if text == "حذف قناة الاشتراك الاجباري" or message.text == "حذف قناة الاشتراك":
                data.delete(bot_id+"-mediapy-channel")
                bot("sendMessage",{"chat_id":chat_id,"text":"*تم حذف قناة الاشتراك الاجباري بنجاح*","parse_mode":"MarkDown","reply_to_message_id":message_id})

def t_start(client,message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id
    if text:
        if str(user_id) == str(sudo):
            if text in ["تعين كليشة ستارت","تعيين كليشة ستارت"]:
                data.set(bot_id+"-mediapy-start-text","True")
                app.send_message(chat_id=chat_id,reply_to_message_id=message.message_id,text="حسنا عزيزي , الان ارسل الكليشة")
            elif text == "حذف كليشة ستارت":
                try:
                    data.delete(bot_id+"-mediapy-start-txt")
                except Exception:
                    pass
                finally:
                    app.send_message(chat_id=chat_id,reply_to_message_id=message.message_id,text="تم حذف كليشة الستارت")
            else:
                try:
                    if data.get(bot_id+"-mediapy-start-text"):
                        if str(data.get(bot_id+"-mediapy-start-text").decode()) == "True":
                            data.set(bot_id+"-mediapy-start-txt",text)
                            app.send_message(chat_id=chat_id,reply_to_message_id=message.message_id,text="تم تعيين هذه الكليشه للستارت")
                except Exception:
                    time.sleep(0.0001)
                finally:
                    data.delete(bot_id+"-mediapy-start-text")

def t_channel(client,message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id
    if text:
        if str(user_id) == str(sudo):
            if text in ["تعين كليشة الاشتراك الاجباري","تعيين كليشة الاشتراك الاجباري"]:
                data.set(bot_id+"-mediapy-channel-text","True")
                app.send_message(chat_id=chat_id,reply_to_message_id=message.message_id,text="حسنا عزيزي , الان ارسل الكليشة")
            elif text == "حذف كليشة الاشتراك الاجباري":
                try:
                    data.delete(bot_id+"-mediapy-txt1")
                except Exception:
                    pass
                finally:
                    app.send_message(chat_id=chat_id,reply_to_message_id=message.message_id,text="تم حذف كليشة الاشتراك")
            else:
                try:
                    if data.get(bot_id+"-mediapy-channel-text"):
                        if str(data.get(bot_id+"-mediapy-channel-text").decode()) == "True":
                            data.set(bot_id+"-mediapy-txt1",text)
                            app.send_message(chat_id=chat_id,reply_to_message_id=message.message_id,text="تم تعيين هذه الكليشه للاشتراك")
                except Exception:
                    time.sleep(0.0001)
                finally:
                    data.delete(bot_id+"-mediapy-channel-text")

def new(client,message):
    chat_id = message.chat.id
    message_id = message.message_id
    chat_type = message.chat.type
    text = message.text
    user_id = message.from_user.id
    adm = ["رفع منظف","رفع مطور","رفع منظف اساسي","اضف مطور","اضف منظف اساسي","اضف منظف"]
    rdm = ["تنزيل منظف","حذف منظف","تنزيل مطور","حذف مطور","تنزيل منظف اساسي","حذف منظف اساسي","مسح المنظفين","مسح المنظفين الاساسين","مسح المنظفين الاساسيين","مسح المطورين"]
    if message.text == "اذاعه" or message.text == "اذاعة":
        if str(user_id) == str(sudo):
            data.set(bot_id+"-mediapy-wait","broad")
            app.send_message(chat_id=chat_id,text="حسنا الان ارسل الرساله التي تريد اذاعتها")
    if text == "المطورين":
        if str(user_id) == str(sudo):
            get_motor = [str(ii.decode()) for ii in data.sinter(bot_id+"-mediapy-motor")]
            get_names = app.get_users(user_ids=get_motor)
            kk = 0
            ui = 1
            uu = []
            while kk < len(get_motor):
                k = f"{str(ui)} - [{get_names[kk].first_name}](tg://user?id={get_motor[kk]})"
                uu.append(k)
                kk += 1
                ui += 1
            res = "\n".join(uu) if data.sinter(bot_id+"-mediapy-motor") else "لا يوجد مطورين !"
            bot("sendMessage",{
                "chat_id": chat_id,
                "text": res,
                "reply_to_message_id": message_id,
                "parse_mode": "MarkDown"
            })
    if chat_type == "private":
        if str(user_id) == str(sudo):
            if text == "مسح المطورين":
                txt = str(str(text).split(sep=" ")[1])
                data.delete(bot_id+"-mediapy-motor")
                bot('sendMessage',{"chat_id":chat_id,"text":"تم مسح المطورين بنجاح","reply_to_message_id":message_id,"parse_mode":"MarkDown"})
            elif text == "رفع مطور" or text == "اضف مطور":
                data.set(bot_id+"-mediapy-wait","True")
                bot('sendMessage',{"chat_id":chat_id,"text":"حسنا عزيزي الان قم بارسال معرف الشخص","reply_to_message_id":message_id,"parse_mode":"MarkDown"})
            elif text == "تنزيل مطور" or text == "حذف مطور":
                data.set(bot_id+"-mediapy-wait","False")
                bot('sendMessage',{"chat_id":chat_id,"text":"حسنا عزيزي الان قم بارسال معرف الشخص","reply_to_message_id":message_id,"parse_mode":"MarkDown"})
        try:
            if str(data.get(bot_id+"-mediapy-wait").decode()) == "True":
                if re.match("^\d{10}$",str(text)) and not re.match("\s",str(text)):
                    gget = app.get_users(text)
                    if gget:
                        txt = f" تم رفع العضو {gget.first_name} مطور بنجاح"
                        data.sadd(bot_id+"-mediapy-motor",str(message.text))
                    else:
                        txt = "الايدي خاطئ !"
                    bot('sendMessage',{"chat_id":chat_id,"text":txt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                    data.delete(bot_id+"-mediapy-wait")
                elif re.match("^@(.*)$",str(message.text)) and not re.match("\s",str(message.text)):
                    user = app.get_users(str(message.text))
                    if user:
                        txt = f" تم رفع العضو {user.first_name} مطور بنجاح"
                        data.sadd(bot_id+"-mediapy-motor",str(user.id))
                    else:
                        txt = "المعرف خاطئ !"
                    bot('sendMessage',{"chat_id":chat_id,"text":txt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                    data.delete(bot_id+"-mediapy-wait")
            elif str(data.get(bot_id+"-mediapy-wait").decode()) == "False":
                if re.match("^\d{10}$",str(message.text)) and not re.match("\s",str(message.text)):
                    user = app.get_users(str(message.text))
                    if user:
                        txt = f" تم تنزيل العضو {user.first_name} مطور بنجاح"
                        data.srem(bot_id+"-mediapy-motor",str(user.id))
                    else:
                        txt = "الايدي خاطئ !"
                    bot('sendMessage',{"chat_id":chat_id,"text":txt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                    data.delete(bot_id+"-mediapy-wait")
                elif re.match("^@(.*)$",str(message.text)) and not re.match("\s",str(message.text)):
                    user = app.get_users(str(message.text))
                    if user:
                        txt = f" تم تنزيل العضو {user.first_name} مطور بنجاح"
                        data.srem(bot_id+"-mediapy-motor",str(user.id))
                    else:
                        txt = "المعرف خاطئ !"
                    bot('sendMessage',{"chat_id":chat_id,"text":txt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                    data.delete(bot_id+"-mediapy-wait")

        except Exception:
            pass
    if chat_type == "group" or chat_type == "supergroup":
        if str(user_id) == str(sudo):
            if text == "مسح المطورين":
                if channel(user_id):
                    txt = str(str(text).split(sep=" ")[1])
                    data.delete(bot_id+"-mediapy-motor")
                    bot('sendMessage',{"chat_id":chat_id,"text":"تم مسح المطورين بنجاح","reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                else:
                    channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                    txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                    txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                    res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                    bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        if text in ["الأوامر","ألاوامر","ألأوامر","الاوامر"]:
            if channel(user_id):
                if admins(chat_id,user_id):
                    txt = "1 - تفعيل / تعطيل  ~ للمشرفين\n2 - امسح / تنظيف ~ للمنظفين\n3 - تفعيل / تعطيل التلقائي ~ للاساسيين\n4 - عدد المسح ~ للاساسيين\n5 - الميديا -- لعرض عدد الميديا انلاين ~ للمنظف\n6 - رفع / تنزيل منظف اساسي ~ للمالك\n7 - رفع / تنزيل منظف ~ للمنظف الاساسي\n8 - المنظفين الاساسيين ~ للمالك\n9 - المنظفين ~ للمنظف الاساسي"
                    app.send_message(chat_id=chat_id,text=txt,reply_to_message_id=message_id,parse_mode="MarkDown")
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        if text == "المنظفين الاساسيين " or text == "المنظفين الاساسين":
            if channel(user_id):
                if sudos(chat_id,user_id):
                    t = [str(i.decode()) for i in data.sinter(bot_id+"-mediapy-su-"+str(chat_id))]
                    get_names = app.get_users(user_ids=t)
                    kk = 0
                    ui = 1
                    uu = []
                    while kk < len(t):
                        k = f"{str(ui)} - [{get_names[kk].first_name}](tg://user?id={t[kk]})"
                        uu.append(k)
                        kk += 1
                        ui += 1
                    res = "\n".join(uu) if data.sinter(bot_id+"-mediapy-su-"+str(chat_id)) else "لا يوجد منظفين اساسيين !"
                    bot("sendMessage",{
                        "chat_id": chat_id,
                        "text": res,
                        "reply_to_message_id": message_id,
                        "parse_mode": "MarkDown"
                    })
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        if text == "المنظفين" or text == "المنضفين":
            if channel(user_id):
                if manager(chat_id,user_id):
                    t = [str(i.decode()) for i in data.sinter(bot_id+"-mediapy-sudos-"+str(chat_id))]
                    get_names = app.get_users(user_ids=t)
                    kk = 0
                    ui = 1
                    uu = []
                    while kk < len(t):
                        k = f"{str(ui)} - [{get_names[kk].first_name}](tg://user?id={t[kk]})"
                        uu.append(k)
                        kk += 1
                        ui += 1
                    res = "\n".join(uu) if data.sinter(bot_id+"-mediapy-sudos-"+str(chat_id)) else "لا يوجد منظفين !"
                    bot("sendMessage",{
                        "chat_id": chat_id,
                        "text": res,
                        "reply_to_message_id": message_id,
                        "parse_mode": "MarkDown"
                    })
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        elif text == "مسح المنظفين":
            if channel(user_id):
                if manager(chat_id,user_id):
                    data.delete(bot_id+"-mediapy-sudos-"+str(chat_id))
                    bot('sendMessage',{"chat_id":chat_id,"text":"تم مسح المنظفين بنجاح","reply_to_message_id":message_id,"parse_mode":"MarkDown"})
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        elif text == "مسح المنظفين الاساسين" or text == "مسح المنظفين الاساسيين":
            if channel(user_id):
                if sudos(chat_id,user_id):
                    data.delete(bot_id+"-mediapy-su-"+str(chat_id))
                    bot('sendMessage',{"chat_id":chat_id,"text":"تم مسح المنظفين الاساسيين بنجاح","reply_to_message_id":message_id,"parse_mode":"MarkDown"})
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        if text == "رفع مطور" or text == "اضف مطور":
            if str(user_id) == str(sudo):
                if message.reply_to_message:
                    user = str(message.reply_to_message.from_user.id)
                    data.sadd(bot_id+"-mediapy-motor",user)
                    txtt = f"تم رفع العضو [{str(message.reply_to_message.from_user.first_name)}](tg://user?id={user}) مطور بنجاح"
                    bot('sendMessage',{"chat_id":chat_id,"text":txtt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
        elif text == "تنزيل مطور" or text == "حذف مطور":
            if str(user_id) == str(sudo):
                if message.reply_to_message:
                    user = str(message.reply_to_message.from_user.id)
                    data.srem(bot_id+"-mediapy-motor",user)
                    txtt = f"تم تنزيل العضو [{str(message.reply_to_message.from_user.first_name)}](tg://user?id={str(message.reply_to_message.from_user.id)}) مطور بنجاح"
                    bot('sendMessage',{"chat_id":chat_id,"text":txtt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
        if text == "رفع منظف اساسي" or text == "اضف مطور اساسي":
            if message.reply_to_message:
                if channel(user_id):
                    if sudos(chat_id,user_id):
                        data.sadd(bot_id+"-mediapy-su-"+str(chat_id),str(message.reply_to_message.from_user.id))
                        txtt = f"تم رفع العضو [{str(message.reply_to_message.from_user.first_name)}](tg://user?id={str(message.reply_to_message.from_user.id)}) منظف اساسي بنجاح"
                        bot('sendMessage',{"chat_id":chat_id,"text":txtt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                else:
                    channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                    txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                    txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                    res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                    bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        elif text == "تنزيل منظف اساسي" or text == "حذف منظف اساسي":
            if message.reply_to_message:
                if channel(user_id):
                    if sudos(chat_id,user_id):
                        data.srem(bot_id+"-mediapy-su-"+str(chat_id),str(message.reply_to_message.from_user.id))
                        txtt = f"تم تنزيل العضو [{str(message.reply_to_message.from_user.first_name)}](tg://user?id={str(message.reply_to_message.from_user.id)}) منظف اساسي بنجاح"
                        bot('sendMessage',{"chat_id":chat_id,"text":txtt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                else:
                    channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                    txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                    txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                    res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                    bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        if text == "رفع منظف" or text == "اضف منظف":
            if message.reply_to_message:
                if manager(chat_id,user_id):
                    if channel(user_id):
                        data.sadd(bot_id+"-mediapy-sudos-"+str(chat_id),str(message.reply_to_message.from_user.id))
                        txtt = f"تم رفع العضو [{str(message.reply_to_message.from_user.first_name)}](tg://user?id={str(message.reply_to_message.from_user.id)}) منظف بنجاح"
                        bot('sendMessage',{"chat_id":chat_id,"text":txtt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                    else:
                        channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                        txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                        txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                        res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                        bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        elif text == "تنزيل منظف" or text == "حذف منظف":
            if message.reply_to_message:
                if manager(chat_id,user_id):
                    if channel(user_id):
                        data.srem(bot_id+"-mediapy-sudos-"+str(chat_id),str(message.reply_to_message.from_user.id))
                        txtt = f"تم تنزيل العضو [{str(message.reply_to_message.from_user.first_name)}](tg://user?id={str(message.reply_to_message.from_user.id)}) منظف بنجاح"
                        bot('sendMessage',{"chat_id":chat_id,"text":txtt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                    else:
                        channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                        txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                        txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                        res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                        bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})