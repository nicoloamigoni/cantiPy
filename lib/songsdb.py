import json
import lib.le3it_scraper as le3it_scraper
import random
import string
from lib.songclass import Song

def get_songs():
    le3it_scraper.get_songs_from_le3()
    with open("lib/songs.json", "r") as f:
        songs = Song.load_songs_from_json(f.read())
    
    # order songs by title
    songs.sort(key=lambda x: x.title)
    return songs

def delete_song(song):
    try:
        with open("lib/songs.json", "r") as f:
            existing_songs = Song.load_songs_from_json(f.read())
        
        existing_songs = [s for s in existing_songs if s.link != song.link]
        
        with open("lib/songs.json", "w") as f:
            json.dump([song.__dict__ for song in existing_songs], f, indent=4)
    except FileNotFoundError:
        pass
    
    try:
        with open("lib/exclusions.json", "r") as f:
            exclusions = json.load(f)
        
        exclusions.append(song.link)
        with open("lib/exclusions.json", "w") as f:
            json.dump(exclusions, f, indent=4)
    except FileNotFoundError:
        pass


def update_song(song):
    with open("lib/songs.json", "r") as f:
        existing_songs = Song.load_songs_from_json(f.read())
    
    if(not(len(song.translation)==0 or song.translation[0]=="") and len(song.text) != len(song.translation)):
        return False

    for i, s in enumerate(existing_songs):
        if s.link == song.link:
            existing_songs[i] = song
            break
    
    with open("lib/songs.json", "w") as f:
        json.dump([song.__dict__ for song in existing_songs], f, indent=4)
    return True

def new_song(title, author, lyrics, translation):
    
    id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
    song = Song(title, author, id, translation != "")

    lyrics = lyrics.split("\n\n")
    translation = translation.split("\n\n")

    song.set_text(lyrics)
    song.set_translation(translation)

    if translation!="" and len(lyrics) != len(translation):
        return None
    
    with open("lib/songs.json", "r") as f:
        existing_songs = Song.load_songs_from_json(f.read())
    
    existing_songs.append(song)

    with open("lib/songs.json", "w") as f:
        json.dump([song.__dict__ for song in existing_songs], f, indent=4)
    return song
    