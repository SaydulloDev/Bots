from datetime import datetime

now = datetime.now()


def start_user_msg(first_name):
    return f'Hello {first_name}👋Welcome to Trello.com Bot\n' \
           f'Send me command /auth for authorize Trello'


AUTH = 'Send Trello Username:'
ADDED = 'Added Successfully.'
CANCEL = 'Canceled.'
BOARDS = 'Select Board:'
TRELLO_USER_NOT_FOUND = 'Username Not Found!'
ALREADY_REG = 'You are registered!'
NO_TASK = 'Task Not Found!'
CREATE_TASK = 'Select Board for Creating Task'
TASK_NAME = 'Send Task Name:'
TASK_DES = 'Send Task Description:'
TASK_MEMBERS = 'To whom is the task attached?\nSend Name:'
LABELS = 'Select Label:'
TASK_DEADLINE = f'Task Deadline:\nEx: {now.strftime("%Y-%m-%d")}'