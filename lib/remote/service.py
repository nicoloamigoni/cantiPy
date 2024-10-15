from flask import Flask, jsonify
from flask import Flask, jsonify, request
from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
songs = [
    {'id': 1, 'title': 'Song 1', 'artist': 'Artist 1'},
    {'id': 2, 'title': 'Song 2', 'artist': 'Artist 2'},
    {'id': 3, 'title': 'Song 3', 'artist': 'Artist 3'}
]

# Get all songs
@app.route('/songs', methods=['GET'])
def get_songs():
    return jsonify(songs)

# Get a specific song
@app.route('/songs/<int:song_id>', methods=['GET'])
def get_song(song_id):
    song = next((song for song in songs if song['id'] == song_id), None)
    if song:
        return jsonify(song)
    return jsonify(message='Song not found'), 404

# Create a new song
@app.route('/songs', methods=['POST'])
def create_song():
    new_song = {
        'id': len(songs) + 1,
        'title': request.json.get('title'),
        'artist': request.json.get('artist')
    }
    songs.append(new_song)
    return jsonify(new_song), 201

# Update an existing song
@app.route('/songs/<int:song_id>', methods=['PUT'])
def update_song(song_id):
    song = next((song for song in songs if song['id'] == song_id), None)
    if song:
        song['title'] = request.json.get('title', song['title'])
        song['artist'] = request.json.get('artist', song['artist'])
        return jsonify(song)
    return jsonify(message='Song not found'), 404

# Delete a song
@app.route('/songs/<int:song_id>', methods=['DELETE'])
def delete_song(song_id):
    global songs
    songs = [song for song in songs if song['id'] != song_id]
    return jsonify(message='Song deleted')

# Convert songs to PDFs
@app.route('/songs/pdf', methods=['GET'])
def convert_songs_to_pdf():
    pdfs = []
    for song in songs:
        pdf = pdf_generator.generate_pdf(song)
        pdfs.append(pdf)
    return jsonify(pdfs)

if __name__ == '__main__':
    app.run()