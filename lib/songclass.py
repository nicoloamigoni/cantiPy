import json
# Create the Song class
class Song:
    def __init__(self, title, author, link, isForeign):
        self.title = title
        self.author = author
        self.link = link
        self.isForeign = isForeign
        self.text = None
        self.translation = None

        if self.isForeign:
            self.translation = ""

    def set_text(self, text):
        self.text = text

    def set_translation(self, translation):
        self.translation = translation

    @classmethod
    def load_songs_from_json(cls, json_data):
        data_list = json.loads(json_data)
        songs = []
        for data in data_list:
            song = Song.from_json(data)
            songs.append(song)
        return songs
    
    @classmethod
    def from_json(cls, data):
        song = cls(data["title"], data["author"], data["link"], data["isForeign"])
        song.text = data["text"]
        song.translation = data["translation"]
        return song
    
    def __str__(self):
        return f"{self.title} by {self.author}"
        