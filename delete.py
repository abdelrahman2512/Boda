from multiprocessing.pool import ThreadPool as Pool
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import redis
import json
from utils.config import bot_id
from utils.func import bot,app,admins,channel_id,channel


data = redis.Redis("127.0.0.1",6379)

def delete(client,message):
    chat_id = message.chat.id
    message_id = message.message_id
    chat_type = message.chat.type
    user_id = message.from_user.id
    first = str(message.from_user.first_name)
    invite = app.get_chat(chat_id).invite_link
    text = message.text
    if chat_type == "group" or chat_type == "supergroup":
        if text in ["تنظيف","امسح"]:
            if channel(str(user_id)):
                if data.sismember(bot_id+"-mediapy-chats",str(chat_id)):
                    if admins(chat_id,user_id):
                        try:
                            gmsgs = data.sinter(bot_id+"-mediapy-msg-"+str(chat_id))
                            if gmsgs:
                                txt = f"*تم حذف {str(len(gmsgs))} من الميديا !*"
                                msgs = [int(k.decode()) for k in gmsgs]
                                pool = Pool(int(len(msgs)))
                                for i in pool.imap_unordered(lambda x:app.delete_messages(chat_id=chat_id,message_ids=x),msgs):
                                    print(i)
                            else:
                                txt = "*لا توجد ميديا لحذفها !*"
                        except Exception:
                            pass
                        finally:
                            bot("sendMessage",{"chat_id":chat_id,"text":txt,"parse_mode":"MarkDown","reply_to_message_id":message_id})
                            data.delete(bot_id+"-mediapy-video"+str(chat_id),str(message_id))
                            data.delete(bot_id+"-mediapy-anima"+str(chat_id),str(message_id))
                            data.delete(bot_id+"-mediapy-sticker-"+str(chat_id),str(message_id))
                            data.delete(bot_id+"-mediapy-photo"+str(chat_id),str(message_id))
                            data.delete(bot_id+"-mediapy-edits-"+str(chat_id),str(message_id))
                            data.delete(bot_id+"-mediapy-msg-"+str(chat_id),str(message_id))
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})
        if message.text == "الميديا" or message.text == "عدد الميديا":
            if channel(user_id):
                    photo = len(data.sinter(bot_id+"-mediapy-photo"+str(chat_id))) if data.sinter(bot_id+"-mediapy-photo"+str(chat_id)) else 0
                    video = len(data.sinter(bot_id+"-mediapy-video"+str(chat_id))) if data.sinter(bot_id+"-mediapy-video"+str(chat_id)) else 0
                    anima = len(data.sinter(bot_id+"-mediapy-anima"+str(chat_id))) if data.sinter(bot_id+"-mediapy-anima"+str(chat_id)) else 0
                    sticker = len(data.sinter(bot_id+"-mediapy-sticker-"+str(chat_id))) if data.sinter(bot_id+"-mediapy-sticker-"+str(chat_id)) else 0
                    gmsgs = len(data.sinter(bot_id+"-mediapy-msg-"+str(chat_id))) if data.sinter(bot_id+"-mediapy-msg-"+str(chat_id)) else 0
                    edits = len(data.sinter(bot_id+"-mediapy-edits-"+str(chat_id))) if data.sinter(bot_id+"-mediapy-edits-"+str(chat_id)) else 0
                    bot("sendMessage",{
                        "chat_id":chat_id,
                        "text":"*عدد الميديا :-*",
                        "parse_mode":"MarkDown",
                        "reply_to_message_id":message_id,
                        "reply_markup":json.dumps({"inline_keyboard":[
                            [
                                {"text":"الصور :- "+str(photo),"callback_data":"photo"},
                                {"text":"مسح الصور","callback_data":"dph"}
                            ],
                            [
                                {"text":"الفيديو :- "+str(video),"callback_data":"video"},
                                {"text":"مسح الفيديوات","callback_data":"dvi"}
                            ],
                            [
                                {"text":"المتحركه :- "+str(anima),"callback_data":"anima"},
                                {"text":"مسح المتحركات","callback_data":"dan"}
                            ],
                            [
                                {"text":"الملصقات :- "+str(sticker),"callback_data":"sticker"},
                                {"text":"مسح الملصقات","callback_data":"dst"}
                            ],
                            [
                                {"text":"الميديا المعدله :- "+str(edits),"callback_data":"edits"},
                                {"text":"مسح الميديا المعدله","callback_data":"ded"}
                            ],
                            [
                                {"text":"جميع الميديا :- "+str(gmsgs),"callback_data":"all"},
                                {"text":"مسح الكل","callback_data":"dall"}
                            ],
                            [
                                {"text":"رجوع","callback_data":"ex"}
                            ]
                        ]})
                    })
            else:
                channel_url = str(app.get_chat(chat_id=channel_id).invite_link)
                txt1 = str(data.get(bot_id+"-mediapy-txt1").decode()) if data.get(bot_id+"-mediapy-txt1") else "*عذرا عزيزي عليك الاشتراك في القناة اولا*"
                txt2 = str(data.get(bot_id+"-mediapy-txt2").decode()) if data.get(bot_id+"-mediapy-txt2") else "اضغط هنا"
                res = InlineKeyboardMarkup([[InlineKeyboardButton(text=txt2,url=channel_url)]])
                bot("sendMessage",{"chat_id":chat_id,"text":txt1,"reply_to_message_id":message_id,"parse_mode":"MarkDown","reply_markup":res})

def callback(client,message):
    chat_id = str(message.message.chat.id)
    user_id = str(message.message.reply_to_message.from_user.id)
    datas = str(message.data)
    photo = data.sinter(bot_id+"-mediapy-photo"+str(chat_id))
    video = data.sinter(bot_id+"-mediapy-video"+str(chat_id))
    anima = data.sinter(bot_id+"-mediapy-anima"+str(chat_id))
    sticker = data.sinter(bot_id+"-mediapy-sticker-"+str(chat_id))
    gmsgs = data.sinter(bot_id+"-mediapy-msg-"+str(chat_id))
    edits = data.sinter(bot_id+"-mediapy-edits-"+str(chat_id))
    if admins(chat_id=chat_id,user_id=user_id):
        if datas:
            if datas == "dph":
                if photo:
                    try:
                        msgs = [int(i.decode()) for i in photo]
                        pool = Pool(len(msgs))
                        for msg in pool.imap_unordered(lambda x:app.delete_messages(chat_id=chat_id,message_ids=x),msgs):
                            print(msg)
                    except Exception:
                        pass
                    finally:
                        bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":f"تم حذف {str(len(msgs))} من الصور","reply_markup":json.dumps(
                            {
                                "inline_keyboard":[
                                    [
                                        {"text":"رجوع","callback_data":"ex"}
                                    ]
                                ]
                            }
                        )})
                        app.edit_message_text(chat_id=chat_id,message_id=message.message.message_id,text=f"تم حذف {str(len(msgs))} من الصور")
                        for i in msgs:
                            data.srem(bot_id+"-mediapy-msg-"+str(chat_id),str(i))
                        data.delete(bot_id+"-mediapy-photo"+str(chat_id))
                        msgs.clear()
                else:
                    bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":"لا توجد صور لحذفها","reply_markup":json.dumps(
                        {
                            "inline_keyboard":[
                                [
                                    {"text":"رجوع","callback_data":"ex"}
                                ]
                            ]
                        }
                    )})
            elif datas == "dvi":
                if video:
                    try:
                        msgs = [int(i.decode()) for i in video]
                        pool = Pool(len(msgs))
                        for msg in pool.imap_unordered(lambda x:app.delete_messages(chat_id=chat_id,message_ids=x),msgs):
                            print(msg)
                    except Exception:
                        pass
                    finally:
                        bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":f"تم حذف {str(len(msgs))} من الفيديوات","reply_markup":json.dumps(
                            {
                                "inline_keyboard":[
                                    [
                                        {"text":"رجوع","callback_data":"ex"}
                                    ]
                                ]
                            }
                        )})
                        for i in msgs:
                            data.srem(bot_id+"-mediapy-msg-"+str(chat_id),str(i))
                        data.delete(bot_id+"-mediapy-video"+str(chat_id))
                        msgs.clear()
                else:
                    bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":"لا توجد فيديوات لحذفها","reply_markup":json.dumps(
                        {
                            "inline_keyboard":[
                                [
                                    {"text":"رجوع","callback_data":"ex"}
                                ]
                            ]
                        }
                    )})
            if datas == "dan":
                if anima:
                    try:
                        msgs = [int(i.decode()) for i in anima]
                        pool = Pool(len(msgs))
                        for msg in pool.imap_unordered(lambda x:app.delete_messages(chat_id=chat_id,message_ids=x),msgs):
                            print(msg)
                    except Exception:
                        pass
                    finally:
                        bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":f"تم حذف {str(len(msgs))} من المتحركات","reply_markup":json.dumps(
                            {
                                "inline_keyboard":[
                                    [
                                        {"text":"رجوع","callback_data":"ex"}
                                    ]
                                ]
                            }
                        )})
                        for i in msgs:
                            data.srem(bot_id+"-mediapy-msg-"+str(chat_id),str(i))
                        ku = 0
                        while ku < 3:
                            try:
                                data.delete(bot_id+"-mediapy-anima"+str(chat_id))
                                msgs.clear()
                                ku+=2
                                break
                            except Exception:
                                ku+=1
                else:
                    bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":"لا توجد متحركات لحذفها","reply_markup":json.dumps(
                        {
                            "inline_keyboard":[
                                [
                                    {"text":"رجوع","callback_data":"ex"}
                                ]
                            ]
                        }
                    )})
            elif datas == "dst":
                if sticker:
                    try:
                        msgs = [int(i.decode()) for i in sticker]
                        pool = Pool(len(msgs))
                        for msg in pool.imap_unordered(lambda x:app.delete_messages(chat_id=chat_id,message_ids=x),msgs):
                            print(msg)
                    except Exception:
                        pass
                    finally:
                        bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":f"تم حذف {str(len(msgs))} من الملصقات","reply_markup":json.dumps(
                            {
                                "inline_keyboard":[
                                    [
                                        {"text":"رجوع","callback_data":"ex"}
                                    ]
                                ]
                            }
                        )})
                        for i in msgs:
                            data.srem(bot_id+"-mediapy-msg-"+str(chat_id),str(i))
                        data.delete(bot_id+"-mediapy-sticker-"+str(chat_id))
                        msgs.clear()
                else:
                    app.edit_message_text(chat_id=chat_id,message_id=message.message.message_id,text="لا توجد ملصقات لحذفها")
            if datas == "ded":
                if edits:
                    try:
                        msgs = [int(i.decode()) for i in edits]
                        pool = Pool(len(msgs))
                        for msg in pool.imap_unordered(lambda x:app.delete_messages(chat_id=chat_id,message_ids=x),msgs):
                            print(msg)
                    except Exception:
                        pass
                    finally:
                        bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":f"تم حذف {str(len(msgs))} من الميديا المعدله","reply_markup":json.dumps(
                            {
                                "inline_keyboard":[
                                    [
                                        {"text":"رجوع","callback_data":"ex"}
                                    ]
                                ]
                            }
                        )})
                        for i in msgs:
                            data.srem(bot_id+"-mediapy-msg-"+str(chat_id),str(i))
                        data.delete(bot_id+"-mediapy-edits-"+str(chat_id))
                        msgs.clear()
                else:
                    app.edit_message_text(chat_id=chat_id,message_id=message.message.message_id,text="لا توجد ميديا معدله لحذفها")
            elif datas == "dall":
                if gmsgs:
                    msgs = [int(i.decode()) for i in gmsgs]
                    try:
                        pool = Pool(len(msgs))
                        for msg in pool.imap_unordered(lambda x:app.delete_messages(chat_id=chat_id,message_ids=x),msgs):
                            print(msg)
                    except Exception:
                        pass
                    finally:
                        bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":f"تم حذف {str(len(msgs))} من الميديا","reply_markup":json.dumps(
                            {
                                "inline_keyboard":[
                                    [
                                        {"text":"رجوع","callback_data":"ex"}
                                    ]
                                ]
                            }
                        )})
                        msgs.clear()
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
                else:
                    bot("editMessageText",{"chat_id":chat_id,"message_id":message.message.message_id,"text":"لا توجد ميديا لحذفها","reply_markup":json.dumps(
                            {
                                "inline_keyboard":[
                                    [
                                        {"text":"رجوع","callback_data":"ex"}
                                    ]
                                ]
                            }
                        )})
            if datas == "ex":
                photo = len(data.sinter(bot_id+"-mediapy-photo"+str(chat_id))) if data.sinter(bot_id+"-mediapy-photo"+str(chat_id)) else 0
                video = len(data.sinter(bot_id+"-mediapy-video"+str(chat_id))) if data.sinter(bot_id+"-mediapy-video"+str(chat_id)) else 0
                anima = len(data.sinter(bot_id+"-mediapy-anima"+str(chat_id))) if data.sinter(bot_id+"-mediapy-anima"+str(chat_id)) else 0
                sticker = len(data.sinter(bot_id+"-mediapy-sticker-"+str(chat_id))) if data.sinter(bot_id+"-mediapy-sticker-"+str(chat_id)) else 0
                gmsgs = len(data.sinter(bot_id+"-mediapy-msg-"+str(chat_id))) if data.sinter(bot_id+"-mediapy-msg-"+str(chat_id)) else 0
                edits = len(data.sinter(bot_id+"-mediapy-edits-"+str(chat_id))) if data.sinter(bot_id+"-mediapy-edits-"+str(chat_id)) else 0
                bot("editMessageText",{
                    "chat_id":chat_id,
                    "text":"*عدد الميديا :-*",
                    "parse_mode":"MarkDown",
                    "message_id":message.message.message_id,
                    "reply_markup":json.dumps({"inline_keyboard":[
                        [
                            {"text":"الصور :- "+str(photo),"callback_data":"photo"},
                            {"text":"مسح الصور","callback_data":"dph"}
                        ],
                        [
                            {"text":"الفيديو :- "+str(video),"callback_data":"video"},
                            {"text":"مسح الفيديوات","callback_data":"dvi"}
                        ],
                        [
                            {"text":"المتحركه :- "+str(anima),"callback_data":"anima"},
                            {"text":"مسح المتحركات","callback_data":"dan"}
                        ],
                        [
                            {"text":"الملصقات :- "+str(sticker),"callback_data":"sticker"},
                            {"text":"مسح الملصقات","callback_data":"dst"}
                        ],
                        [
                            {"text":"الميديا المعدله :- "+str(edits),"callback_data":"edits"},
                            {"text":"مسح الميديا المعدله","callback_data":"ded"}
                        ],
                        [
                            {"text":"جميع الميديا :- "+str(gmsgs),"callback_data":"all"},
                            {"text":"مسح الكل","callback_data":"dall"}
                        ],
                        [
                            {"text":"رجوع","callback_data":"ex"}
                        ]
                    ]})
                })
