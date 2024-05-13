import telebot
from telebot import types
import json
import time
from dbfunctions import Userbase
from flask import Flask, request
import os



app = Flask("SNA Welcome Bot")

def get_config(key):
    # config_file = "/home/prasaanth2k/welcome_bot_sna/src/config.json"  # always use absolute path, not relative path
    # config_file = r"C:\Users\visha\Desktop\sna\welcome_bot_sna-master\src\config.json"
    config_file = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_file, "r") as file:
        config = json.loads(file.read())
    config["app_root_path"] = os.path.dirname(__file__)

    if key in config:
        return config[key]
    else:
        raise Exception("Key {} is not found in config.json".format(key))

TOKEN = get_config("bot_token")
bot = telebot.TeleBot(TOKEN)

@app.route("/setWebhook")
def set_webhook():
    bot.delete_webhook()
    bot.set_webhook(url=get_config("webhook_url"))
    return 'ok'

@app.route("/webhook",methods=['POST','GET'])
def webhook():
    bot.process_new_updates(
        [telebot.types.Update.de_json(request.get_json(force=True))]
    ) 
    return 'ok'


class botmanage:
    @staticmethod
    @bot.message_handler(content_types=["new_chat_members"])
    def greet_new_user(message: telebot.types.Message):
        for new_user in message.new_chat_members:
            if not new_user.is_bot:
                full_name = new_user.first_name
                if new_user.last_name:
                    full_name += f" {new_user.last_name}"
                group_id = message.chat.id
                user_id = new_user.id
                username = new_user.username
                is_bot = new_user.is_bot
                location = message.location
                profile_link = f"https://t.me/{username}" if username else None
                epoctime = int(time.time())
                contact_info = message.contact
                phone_number = None
                if contact_info:
                    phone_number = contact_info.phone_number
                Userbase().add_user_details(
                    full_name=full_name,
                    group_id=group_id,
                    user_id=user_id,
                    user_name=username,
                    epoctime=epoctime,
                    is_bot=is_bot,
                    location=location,
                    profile_link=profile_link,
                    phone_number=phone_number,
                )
                deep_link_url = f"https://t.me/sna_welcome_bot?start={new_user.id}"
                welcome_message = (
                    f"🌟 Welcome,{full_name}! 🌟\n\n"
                    f"Click [here]({deep_link_url}) to grab your welcome kit and kickstart your journey with us. Let's learn and grow together! 🚀"
                )
                # Note: We use parse_mode='Markdown' to enable URL formatting
                bot.send_message(
                    message.chat.id, welcome_message, parse_mode="Markdown"
                )

    @staticmethod
    @bot.message_handler(commands=["start"])
    def handle_start(message:telebot.types.Message):
        print("start command received")
        if message.chat.type != "private":
            bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
        else:
            message_id = message.from_user.id
            Userbase().update_if_triggerd(message_id)
            user = message.from_user
            first_name = user.first_name
            last_name = user.last_name
            if last_name is not None:
                full_name = first_name + last_name
            else:
                full_name = first_name
            username = user.username
            user_id = user.id
            group_id = user.id
            epoctime = int(time.time())
            is_bot = user.is_bot
            location = message.location
            profile_link = f"https://t.me/{username}" if username else None
            contact_info = message.contact
            phone_number = None
            if contact_info:
                phone_number = contact_info.phone_number
            Userbase().only_in_group(
                full_name=full_name,
                group_id=group_id,
                user_id=user_id,
                user_name=username,
                epoctime=epoctime,
                is_bot=is_bot,
                location=location,
                profile_link=profile_link,
                phone_number=phone_number,
            )
            new_member = message.from_user
            if new_member.last_name is not None:
                full_name = new_member.first_name + " " + new_member.last_name
            else:
                full_name = new_member.first_name
            welcome_message_path = os.path.join(get_config('app_root_path'),get_config("welcome_message"))
            general_message_path = os.path.join(get_config('app_root_path'),get_config("general_message"))
            with open(welcome_message_path, "r", encoding="utf-8") as mg:
                welcome_message_template = mg.read()
            with open(general_message_path,"r",encoding="utf-8") as gm:
                general_message_template = gm.read()
            username = new_member.username
            course_name = Userbase().group_id_get(username)
            # print(group_id)
            # main_groupid = group_id.get('group_id')
            # course_name = get_config('group_id').get(str(main_groupid))
            print(course_name)
            if course_name == "None":
                welcome_message = general_message_template.format(first_name=full_name)
            else:
                welcome_message = welcome_message_template.format(course_name=course_name,first_name=full_name)
            bot.send_message(message.chat.id, welcome_message)
            filepath = os.path.join(get_config('app_root_path'),get_config("sop_file_path"))
            thumnail = os.path.join(get_config('app_root_path'),get_config("thumnail"))        
            with open(thumnail, "rb") as thumb:
                image = thumb.read()
            with open(filepath, "rb") as sop:
                bot.send_document(
                    message.chat.id, sop, caption="Kindly read this first", thumbnail=image
                )


if __name__ == '__main__':
    print("[*] Starting Bot...")
    app.run(host="0.0.0.0", port=80)
# try:
#     bot.polling(none_stop=True)
# except KeyboardInterrupt:
#     print("[*] Keyboard Interrupted ")