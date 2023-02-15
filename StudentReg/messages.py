START_MSG = 'Assalomu Alaykum\nStudentReg botga Xush Kelibsiz\nRoyhatdan otish uchun /reg buyrugini yuboring'
FIRST_NAME = 'Ismingizni Kiriting:'
LAST_NAME = 'Familyangizni Kiriting:'
AGE = 'Yoshingizni Kiriting:'
ADDRESS = 'Manzilingizni kiriting:'
COURSE_ = 'Kurs tanlang:'
TIME_COURSE = 'Kurs otish vaqti:'
LANG_COURSE = 'Kurs Tilini tanlang:'


def info_user_full(fname, lname, age, address, course, lang, time):
    return f'Your Full Info:\nFirst Name : {fname}\nLast Name : {lname}\n' \
           f'Age : {age}\nAddress : {address}\nCourse : {course}\nLanguage : {lang}\nTime : {time}\n\nConfirm Date!'
