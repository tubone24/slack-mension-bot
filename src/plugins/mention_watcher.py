import re
import requests

from slackbot.bot import respond_to
from slackbot.bot import listen_to


@listen_to(r"(.*)")
def listen_func(message, something):
    message.send("aaa")
    message.reply("bbb")
    print(something)
    user_ids = extract_user_id(something)
    for user_id in user_ids:
        user_name = get_user_name(get_user_list(), user_id)
        print(user_name)


def get_user_list():
    r = requests.get("https://slack.com/api/users.list?token=xxxxxxxxxxxxxxxxxxxxxx").json()
    members_list = r["members"]
    return members_list


def extract_user_id(chat):
    user_id_pattern = "<@[A-Z0-9]{9}>"
    compile_pattern = re.compile(user_id_pattern)
    r = compile_pattern.findall(chat)
    return [user.replace("<", "").replace(">", "").replace("@", "") for user in r]


def get_user_name(user_list, user_id):
    for user in user_list:
        if user["id"] == user_id:
            return user["name"]
