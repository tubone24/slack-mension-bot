import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import requests
import yaml

from slackbot.bot import listen_to


def load_config():
    with open("config.yaml") as f:
        config = yaml.load(f)
        return config


@listen_to(r"(.*)")
def listen_func(message, something):
    config = load_config()
    print(config)
    smtp_cnf = config["smtp"]
    user_cnf = config["user"]
    sender_add = smtp_cnf["sender_add"]
    bcc_add = smtp_cnf["bcc_add"]
    password = smtp_cnf["password"]
    token = config["slack"]["token"]
    print(something)
    user_list = get_user_list(token)
    from_user_id = message.body["user"]
    from_user_name = get_user_name(user_list, from_user_id)
    user_ids = extract_user_id(something)
    for user_id in user_ids:
        to_user_name = get_user_name(user_list, user_id)
        target_add = get_user_mail_add(to_user_name, user_cnf)
        subject = create_subject(from_user_name)
        body = create_body(from_user_name, to_user_name)
        msg = create_mail_message(sender_add, target_add, bcc_add, subject, body)
        send_mail(sender_add, password, target_add, msg)
    message.react("email")


def get_user_list(token):
    r = requests.get("https://slack.com/api/users.list?token=" + token).json()
    members_list = r["members"]
    return members_list


def create_mail_message(from_addr, to_addr, bcc_addrs, subject, body):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = to_addr
    msg["Bcc"] = bcc_addrs
    msg["Date"] = formatdate()
    return msg


def create_body(from_user_name, to_user_name):
    body = "Slackに{from_user_name}さんから" \
           "あなた({to_user_name})宛にメンションがあります\n" \
           "Slackを開いて内容を確認してね".format(from_user_name=from_user_name, to_user_name=to_user_name)
    return body


def create_subject(from_user_name):
    body = "Slackに{user}さんからメンションがあります".format(user=from_user_name)
    return body


def extract_user_id(chat):
    user_id_pattern = "<@[A-Z0-9]{9}>"
    compile_pattern = re.compile(user_id_pattern)
    r = compile_pattern.findall(chat)
    return [user.replace("<", "").replace(">", "").replace("@", "") for user in r]


def get_user_name(user_list, user_id):
    for user in user_list:
        if user["id"] == user_id:
            return user["name"]
    return False


def send_mail(from_addr, password, to_addrs, msg):
    smtpobj = smtplib.SMTP("smtp.gmail.com", 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(from_addr, password)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


def get_user_mail_add(user_name, user_config):
    for user in user_config:
        if user["name"] == user_name:
            return user["mail"]
        else:
            return None

