from pytube import YouTube


def send_info(url):
    yt = YouTube(url)
    return yt
