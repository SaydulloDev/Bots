from pytube import YouTube


def send_info(url):
    yt = YouTube(url)
    return yt


def download_video720(url):
    yt = YouTube(url)
    video = yt.streams.filter(res='720p').first()
    video.download('./')
    return video.default_filename


def download_video480(url):
    yt = YouTube(url)
    video = yt.streams.filter(res='480p').first()
    video.download('./')
    return video.default_filename
