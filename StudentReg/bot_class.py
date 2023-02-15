class Chat:
    def __init__(self, chat_id, first_name, lang_code):
        self.chat_id = chat_id
        self.first_name = first_name
        self.lang_code = lang_code

    def dict_attrs_func(self):
        return {
            'ChatID': self.chat_id,
            'FirstName': self.first_name,
            'Language': self.lang_code
        }
