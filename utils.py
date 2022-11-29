def is_track(sp_dict: dict) -> bool:
    return sp_dict is not None and sp_dict["currently_playing_type"] == 'track'

def is_playing_track(sp_dict: dict) -> bool:
    return sp_dict is not None and sp_dict["is_playing"]

def ad_is_playing(sp_dict: dict) -> bool:
    return sp_dict is not None and sp_dict["currently_playing_type"] == 'ad'

def get_duration_ms(sp_dict: dict) -> int:
    return sp_dict["item"]["duration_ms"]

def get_progress_ms(sp_dict: dict) -> int:
    return sp_dict["progress_ms"]

def get_track_name(sp_dict: dict) -> str:
    return sp_dict["item"]["name"]

def get_track_image(sp_dict: dict) -> str:
    return sp_dict["item"]["album"]["images"][0]["url"]

def get_track_id(sp_dict:dict) -> str:
    return sp_dict["item"]["id"]

def get_artist_names(sp_dict: dict) -> list:
    artists = sp_dict["item"]["artists"]
    return [a["name"] for a in artists]

def display_artist_names(artists: list) -> str:
    ret = artists[0]
    if len(artists) == 1:
        return ret
    for name in artists[1:]:
        ret += ', ' + name
    return ret

def timefmt(seconds: int) -> str:
    # h, m, s
    m, s = divmod(seconds, 60)  
    h, m = divmod(m, 60)
    if h == 0:
        return f"{m:02d}:{s:02d}"
    return f"{h:d}:{m:02d}:{s:02d}"