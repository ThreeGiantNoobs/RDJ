import traceback
from interactions.api.voice.audio import AudioVolume

from dataFunc import search


def get_song(query: str) -> (AudioVolume, str):
    try:
        url, video_link = search(query)
        audio = AudioVolume(url)
        audio.volume = 0.2

        return audio, video_link
    except Exception as e:
        print(e)
        traceback.print_exc()
