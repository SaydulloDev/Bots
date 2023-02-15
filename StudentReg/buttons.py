from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

COURSE = {
    'Python': 'Python',
    'Java': 'Java',
    'Flutter': 'Flutter',
    'Frontend': 'Frontend',
}
LANGUAGE = {
    'Uzbek🇺🇿': 'Uzbek🇺🇿',
    'Russia🇷🇺': 'Russia🇷🇺',
    'English🏴󠁧󠁢󠁥󠁮󠁧󠁿': 'English🏴󠁧󠁢󠁥󠁮󠁧󠁿'
}
TIME_COURSE = {
    '09:00': '09',
    '15:00': '15',
    '19:00': '19'
}
CONFIRM = {
    'Yes✔': 'yes',
    'No❌': 'no'
}
# Course Select Button
course_buttons = InlineKeyboardMarkup()
for k, v in COURSE.items():
    course_buttons.add(
        InlineKeyboardButton(k, callback_data=f"course_{v}")
    )
# Language Select Button
language_buttons = InlineKeyboardMarkup()
for k1, v1 in LANGUAGE.items():
    language_buttons.add(
        InlineKeyboardButton(k1, callback_data=f"lang_{v1}")
    )

time_buttons = InlineKeyboardMarkup()
for k3, v3 in TIME_COURSE.items():
    time_buttons.add(
        InlineKeyboardButton(k3, callback_data=f"time_{v3}")
    )

confirm_buttons = InlineKeyboardMarkup()
for k4, v4 in CONFIRM.items():
    confirm_buttons.add(
        InlineKeyboardButton(k4, callback_data=f'answer_{v4}')
    )
