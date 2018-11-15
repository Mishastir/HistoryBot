import requests
import json
import time
import urllib
from DataBaseHelper import DBHelper
from Quest import Quests

db = DBHelper()
quest = Quests()

Safonov_chat = 360317859
Halk_chat = 405846055
TOKEN = "723144612:AAGoGsa9kKUKZNPzdT9DdQr9HeTqAhTKg4A"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def build_keyboard(items):

    keyboard = [["Так"], ["Ні"]]
    reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)

def handle_updates(updates):
    """" Analyzing updates from server and acting with them """
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            items = db.get_items()
            if text == "/startquest":
                send_message("Вітаємо на квесті!", chat)
                time.sleep(2)
                send_message("Ваше перше питання:\n" + items[0], chat)
                quest.started = True
            if (text[0] != '/' or text == "/endquest") and quest.started:
                result = quest.main(items, text)
                if result != 0:
                    send_message(result, chat)
                    next_question = quest.next_question(items, text)
                    if next_question != 0 and quest.started and quest.go_forward:
                        time.sleep(3)
                        send_message(next_question, chat)
                else:
                    keyboard = build_keyboard(items)
                    send_message("Ваша відповідь 3й раз підряд не вірна, може вам потрібна підказка?", chat, keyboard)
        except KeyError:
            pass

def main():
    """" Starting our bot, initializing database and starting infinity loop for catching updates """
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates)+1
            handle_updates(updates)
        #time.sleep(0.5)

def get_url(url):
    """" Getting url """
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    """ Extracting json from url """
    content = get_url(url)
    js = json.loads(content)
    return js

def get_last_update_id(updates):

    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_updates(offset=None):
    url = URL+"getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_chat_id_and_text(updates):
    """ To act only with updates, we haven`t worked before, we take last update id """
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    get_url(url)

def second_main():
    for a in range(10):
        send_message("Ты бяка", Halk_chat)

if __name__ == '__main__':
    #second_main()
    main()


text, chat = get_last_chat_id_and_text(get_updates())
send_message(text, chat)