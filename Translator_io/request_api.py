import requests


def translate(lang_code, text_user):
    source_text = text_user
    target_language = lang_code
    response = requests.get(
        f"https://translate.google.com/translate_a/single?client=gtx&sl=auto&tl={target_language}&dt=t&q={source_text}")
    result = response.json()[0][0][0]
    return result
