import re
import yt_dlp


YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': True, 'cachedir': False, 'nocheckcertificate': True}

yt_link_pat = re.compile(r'(?:https?://)?(?:www\.)?youtu(?:be)?\.(?:com|be)(?:/watch/?\?v=|/embed/|/shorts/|/)(\w+)')
spotify_pattern = re.compile(r'(?:https?://)?(?:www\.)?open\.spotify\.com/track/(\w+)')
spotify_playlist_pattern = re.compile(r'(?:https?://)?(?:www\.)?open\.spotify\.com/playlist/(\w+)')


def search(query):
    query = get_url(query)
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        response = ydl.extract_info(f"ytsearch: {query}", download=False)['entries'][0]
        video_url, video = response['url'], response['webpage_url']
    return video_url, video


def get_url(url):
    match = re.match(yt_link_pat, url)
    spotify_match = re.match(spotify_pattern, url)
    spotify_playlist_match = re.match(spotify_playlist_pattern, url)
    if match:
        return f'"{match[1]}"'
    elif spotify_match:
        return None
    elif spotify_playlist_match:
        return "dQw4w9WgXcQ"
        # return get_tracks_from_spotify_playlist(spotify_playlist_match[1])
    else:
        return url
