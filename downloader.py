from pytube import YouTube
import os

def download_video(url, only_audio=False):
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=only_audio).order_by('abr' if only_audio else 'resolution').desc().first()
    out_file = stream.download()
    base, ext = os.path.splitext(out_file)
    
    if only_audio:
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        return new_file
    return out_file
