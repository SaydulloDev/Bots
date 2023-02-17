import os
import csv


def write_chat_csv(file_path, message):
    header = ["chat_id", "first_name", "last_name", "trello_username"]
    row = {
        "chat_id": message.chat.id,
        "first_name": message.from_user.first_name,
        "last_name": message.from_user.last_name,
        "trello_username": message.text
    }
    with open(file_path, "a+", newline="\n") as f:
        csv_writer = csv.DictWriter(f, header)
        if os.path.getsize(file_path) == 0:
            csv_writer.writeheader()
        csv_writer.writerow(row)
    print("Successfully.")


def get_trello_user(file_path, chat_id):
    with open(file_path, encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        users = [
            row.get('trello_username')
            for row in csv_reader
            if int(row.get('chat_id')) == chat_id
        ]
        return users[0] if users else None


def get_trello_username_by_chat_id(file_path, chat_id):
    with open(file_path, encoding="utf-8") as f:
        csv_reader = csv.DictReader(f)
        users = [
            row.get("trello_username")
            for row in csv_reader
            if int(row.get("chat_id")) == chat_id
        ]
        return users[0] if users else None


def get_member_task_message(card_data, member_id):
    msg = ""
    for data in card_data:
        if member_id in data.get('idMembers'):
            msg += f"{data.get('idShort')} - <a href=\"{data.get('url')}\">{data.get('name')}</a>\n"

        return msg