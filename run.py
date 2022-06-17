import datetime
from utils.func import bot,app,admins,motors,manager,sudos,channel_id,channel
import redis
from utils.config import sudo,token,bot_id
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
from handlers.admins import del_c, new, broad, c_count, s_channel, t_start, t_channel, del_c
from handlers.delete import delete,callback
from threading import Thread
from handlers.start import rstart

data = redis.Redis("127.0.0.1",6379)

@app.on_message()
def one(client,message):
    if data.sismember(bot_id+"-mediapy-auto",str(message.chat.id)):
        ttii = str(data.get(bot_id+"mediapy-time-"+str(message.chat.id)).decode())
        tti = ttii.split(sep=":")[0]
        minute = ttii.split(sep=":")[1]
        if str(datetime.datetime.now().hour) != str(tti) and str(datetime.datetime.now().minute) == str(minute):
            gmsgs = data.sinter(bot_id+"-mediapy-msg-"+str(message.chat.id))
            if gmsgs:
                try:
                    msgs = [int(k.decode()) for k in gmsgs]
                    lmsg = int(data.get(bot_id+"-auto-cmsgs-"+str(message.chat.id)).decode()) if data.get(bot_id+"-auto-cmsgs-"+str(message.chat.id)) else 100000
                    try:
                        kif = len(msgs)
                    except Exception:
                        kif = 0
                    msg = msgs if kif == lmsg or kif < lmsg else msgs[:lmsg]
                    print(list(map(lambda x: app.delete_messages(chat_id=message.chat.id,message_ids=x),msg)))
                except Exception:
                    pass
                finally:
                    data.delete(bot_id+"mediapy-time-"+str(message.chat.id))
                    data.set(bot_id+"mediapy-time-"+str(message.chat.id),str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute))
                    txt = f"*تم حذف {str(kif)} من الميديا !*"
                    bot("sendMessage",{"chat_id":str(message.chat.id),"text":txt,"parse_mode":"MarkDown"})
                    try:
                        data.delete(bot_id+"-mediapy-msg-"+str(chat_id))
                    except Exception:
                        pass
                    try:
                        data.delete(bot_id+"-mediapy-sticker-"+str(chat_id))
                    except Exception:
                        pass
                    try:
                        data.delete(bot_id+"-mediapy-anima"+str(chat_id))
                    except Exception:
                        pass
                    try:
                        data.delete(bot_id+"-mediapy-photo"+str(chat_id))
                    except Exception:
                        pass
                    try:
                        data.delete(bot_id+"-mediapy-video"+str(chat_id))
                    except Exception:
                        pass
                    try:
                        data.delete(bot_id+"-mediapy-edits-"+str(chat_id))
                    except Exception:
                        pass
                    msgs.clear()
    if str(message.chat.type) == "private":
        members = [str(i.decode()) for i in data.sinter(bot_id+"-mediapy-members")]
        if str(message.from_user.id) in members:        
            pass
        else:               
            data.sadd(bot_id+"-mediapy-members",str(message.from_user.id))
    t = Thread(target=rstart,args=(client,message))
    t1 = Thread(target=broad,args=(client,message))
    t2 = Thread(target=c_count,args=(client,message))
    t3 = Thread(target=s_channel,args=(client,message))
    t4 = Thread(target=t_channel,args=(client,message))
    t5 = Thread(target=t_start,args=(client,message))
    t6 = Thread(target=del_c,args=(client,message))
    st1 = Thread(target=new,args=(client,message))
    st2 = Thread(target=delete,args=(client,message))
    t.daemon = True
    t1.daemon = True
    t2.daemon = True
    t3.daemon = True
    t4.daemon = True
    t5.daemon = True
    t6.daemon = True
    st1.daemon = True
    st2.daemon = True
    t.start()
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    st1.start()
    st2.start()
    chat_id = message.chat.id
    message_id = message.message_id
    chat_type = message.chat.type
    first = str(message.from_user.first_name)
    invite = app.get_chat(chat_id).invite_link
    if message.media and message.edit_date and not message.audio and not message.voice and str(chat_type) in ["group","supergroup"]:
        print(message)
        if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
            data.sadd(bot_id+"-mediapy-msg-"+str(chat_id),str(message_id))
            data.sadd(bot_id+"-mediapy-edits-"+str(chat_id),str(message_id))
    user_id = message.from_user.id
    status = bot("getChatMember",{"chat_id":chat_id,"user_id":user_id})['result']['status']
    is_status = True if str(status) == "creator" or str(status) == "administrator" or str(user_id) == str(sudo) else False
    if message.media and not message.voice and not message.audio:
        if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
            if message.photo:
                data.sadd(bot_id+"-mediapy-photo"+str(chat_id),str(message_id))
            elif message.video or message.video_note:
                data.sadd(bot_id+"-mediapy-video"+str(chat_id),str(message_id))
            elif message.animation:
                data.sadd(bot_id+"-mediapy-anima"+str(chat_id),str(message_id))
            elif message.sticker:
                data.sadd(bot_id+"-mediapy-sticker-"+str(chat_id),str(message_id))
            data.sadd(bot_id+"-mediapy-msg-"+str(chat_id),str(message_id))
    if message:
        if chat_type == "private":
            if str(message.from_user.id) not in [str(k.decode()) for k in data.sinter(bot_id+"-mediapy-members")]:
                data.sadd(bot_id+"-mediapy-members",str(message.from_user.id))
    if chat_type == "group" or chat_type == "supergroup":
        if message.text:
            if message.text == "تفعيل":
                if channel(user_id):
                    if is_status:
                        if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
                            txt = "*البوت مفعل بالمجموعه بالتأكيد !*"
                        else:
                            data.sadd(bot_id+"-mediapy-chats",str(chat_id))
                            if not sudos(chat_id=chat_id,user_id=user_id):
                                data.sadd(bot_id+"-mediapy-su-"+str(chat_id),str(user_id))
                            txt = "*تم تفعيل البوت في المجموعه*"
                            title = str(message.chat.title)
                            ttxt = f"*تم تفعيل البوت في المجموعه (( {title} ))\nبواسطة :-* [{first}](tg://user?id={user_id})"
                            bot("sendMessage",{"chat_id":sudo,"text":ttxt,"parse_mode":"MarkDown","disable_web_page_preview":True,"reply_markup":json.dumps({"inline_keyboard":[[{"text":"رابط المجموعه","url":str(invite)}]]})})
                        bot("sendMessage",{"chat_id":chat_id,"text":txt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                    else:
                        bot("sendMessage",{"chat_id":chat_id,"text":"*انت لست ادمن بالمجموعه !*","reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                else:
                    channel_url = str(app.get_chat(channel_id).invite_link)
                    txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                    txt2 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                    res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                    bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
            if message.text == "تعطيل":
                if manager(chat_id,user_id):
                    if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
                        data.srem(bot_id+"-mediapy-chats",str(chat_id))
                        data.srem(bot_id+"-mediapy-auto",str(chat_id))
                        res1 = data.delete(bot_id+"-mediapy-su-"+str(chat_id)) if data.sinter(bot_id+"-mediapy-su-"+str(chat_id)) else print("Not Admins")
                        res2 = data.delete(bot_id+"-mediapy-sudos-"+str(chat_id)) if data.sinter(bot_id+"-mediapy-sudos-"+str(chat_id)) else print("Not Admins")
                        res1
                        res2
                        txt = "*تم تعطيل البوت في المجموعه بنجاح*"
                        title = str(message.chat.title)
                        ttxt = f"*تم تعطيل البوت في المجموعه (( {title} ))\nبواسطة :-* [{first}](tg://user?id={user_id})"
                        bot("sendMessage",{"chat_id":sudo,"text":ttxt,"parse_mode":"MarkDown","disable_web_page_preview":True,"reply_markup":json.dumps({"inline_keyboard":[[{"text":"رابط المجموعه","url":str(invite)}]]})})
                    else:
                        txt = "*البوت معطل بالمجموعه بالتأكيد !*"
                    bot("sendMessage",{"chat_id":chat_id,"text":txt,"reply_to_message_id":message_id,"parse_mode":"MarkDown"})
                else:
                    bot("sendMessage",{"chat_id":chat_id,"text":"*عذرا عزيزي انت لست منظف اساسي في البوت !*","reply_to_message_id":message_id,"parse_mode":"MarkDown"})

@app.on_callback_query()
def call(client,message):
    t = Thread(target=callback,args=(client,message))
    t.daemon = True
    t.start()

app.run()
