import json
import redis
from utils.config import sudo,bot_id
from utils.func import bot


data = redis.Redis("127.0.0.1",6379)

def rstart(client,message):
    chat_id = message.chat.id
    message_id = message.message_id
    chat_type = message.chat.type
    first = str(message.from_user.first_name)
    text = message.text
    user_id = message.from_user.id
    if text == "/start":
        if chat_type == "private":
            if str(user_id) == str(sudo):
                bot("sendMessage",{
                    "chat_id":chat_id,
                    "text":"*أهلا بك عزيزي المطور في لوحة الاوامر*",
                    "reply_to_message_id":message_id,
                    "parse_mode":"MarkDown",
                    "reply_markup":json.dumps({
                        "keyboard":[
                            [
                                {"text":"اذاعه"},
                                {"text":"المطورين"}
                            ],
                            [
                                {"text":"رفع مطور"},
                                {"text":"تنزيل مطور"}
                            ],
                            [
                                {"text":"تعيين قناة الاشتراك الاجباري"},
                                {"text":"حذف قناة الاشتراك الاجباري"}
                            ],
                            [
                                {"text":"تعيين كليشة ستارت"},
                                {"text":"حذف كليشة ستارت"}
                            ],
                            [
                                {"text":"تعيين كليشة الاشتراك الاجباري"},
                                        
                                {"text":"حذف كليشة الاشتراك الاجباري"}
                            ],
                            [
                                {"text":"مسح المطورين"},
                                {"text":"الاحصائيات"}
                            ]
                        ]
                    })
                })
            else:
                txt = str(data.get(bot_id+"-mediapy-start-txt").decode()) if data.get(bot_id+"-mediapy-start-txt") else "*أهلا بك عزيزي في بوت حذف الميديا\nلتفعيل البوت ارفعه مشرف في المجموعه واكتب تفعيل (بصلاحية المالك والمشرفين فقط)*"
                bot("sendMessage",{"chat_id":chat_id,"text":txt,"reply_to_message_id":message_id,"parse_mode":"markdown"})


