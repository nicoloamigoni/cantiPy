import requests
from bs4 import BeautifulSoup
import re
from lib.songclass import Song
import json


def get_song_text(url):
    # Make a GET request to the URL
    response = requests.get(url)

    # Initialize the lists for text and translations
    text_paragraphs = []
    translation_paragraphs = []

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")


        #remove div class="tagscloud" from lyrics_div before proceeding
        tagscloud = soup.find("div", class_="tagscloud")
        if tagscloud:
            tagscloud.decompose()


        # Find the lyrics section
        lyrics_div = soup.find("div", class_="testo", itemprop="lyrics")
        if lyrics_div:
            lyrics_p_tags = lyrics_div.find_all("p")
            for p in lyrics_p_tags:
                # Collect text preserving the breaks
                text_paragraphs.append("\n".join(p.strings))

        # Find the translation section
        translation_div = soup.find("div", class_="trad", itemprop="translationOfWork")
        if translation_div:
            translation_p_tags = translation_div.find_all("p")
            for p in translation_p_tags:
                # Collect text preserving the breaks
                translation_paragraphs.append("\n".join(p.strings))
            if len(translation_paragraphs) == 0:
                translation_paragraphs.append("\n".join(translation_div.strings))
            # Remove "Traduzione:" prefix from the first paragraph, if present
            translation_paragraphs[0] = re.sub(r"^Traduzione:", "", translation_paragraphs[0]).strip()
            translation_paragraphs[0] = re.sub(r"^Traduzione[^\n]*(\r)*\n", "", translation_paragraphs[0]).strip()

    return text_paragraphs, translation_paragraphs


def update_database_with_new_songs(songs):
    try:
        with open("lib/songs.json", "r") as f:
            existing_songs = Song.load_songs_from_json(f.read())
    except FileNotFoundError:
        existing_songs = []    
    try:
        with open("lib/exclusions.json", "r") as f:
            exclusions = json.load(f)
    except FileNotFoundError:
        exclusions = []
    existing_links = [song.link for song in existing_songs]
    new_songs = [song for song in songs if song.link not in existing_links and song.link not in exclusions]

    print("[Info] Found " + str(len(new_songs)) + " new songs.")
    i = 1
    for song in new_songs:
        text, translation = get_song_text(song.link)
        song.set_text(text)
        song.set_translation(translation)
        existing_songs.append(song)
        print("[Info] Song " + str(i) + " of " + str(len(new_songs)) + " added to the database.")
        i += 1

        with open("lib/songs.json", "w") as f:
            json.dump([song.__dict__ for song in existing_songs], f, indent=4)


def get_songs_from_le3():
    # Make a GET request to the URL
    try:
        response = requests.get("https://www.le3.it/loading_canti.php?azione=filtra&search=")

        # Check if the request was successful
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")

            song_links = soup.find_all("a", class_="link_canto_le3")

            songs = []

            for link in song_links:
                full_text = link.get_text(separator=" ", strip=True)
                isForeign = bool(re.search(r'\[traduzione\]', full_text))
                full_text = re.sub(r'\[traduzione\]', '', full_text).strip()

                author_match = re.search(r'\((.*?)\)', full_text)
                author = author_match.group(1).strip() if author_match else None

                title = re.sub(r'\(.*?\)', '', full_text).strip() if author else full_text

                song_link = link["href"]

                song = Song(title, author, song_link, isForeign)
                songs.append(song)
            update_database_with_new_songs(songs)
            # Dump as json file
            print("[Info] Database is up to date and contains " + str(len(songs)) + " songs.")
        else:
            print("[Info] Failed to retrieve the song list.")
    except requests.exceptions.RequestException as e:
        print("[Info] No connection with le3.it, database not updated.")



