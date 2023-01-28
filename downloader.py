import os
from pytube import YouTube


def download(url, only_audio, output_folder):
    yt = YouTube(url)
    if only_audio:
        video = yt.streams.filter(
            only_audio=True
        ).first()
    else:
        video = yt.streams.filter(
            file_extension="mp4",
            only_video=True,
        ).order_by('resolution').desc().first()
    
    out_file = video.download(output_path=output_folder)


    return out_file