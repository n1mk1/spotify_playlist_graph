import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re
import json
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')

# Spotify authentication
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Get Playlist ID
def get_playlist_id(url):
    match = re.search(r'playlist/([a-zA-Z0-9]+)', url) # fianally using some bash holyyyyyyyy
    return match.group(1) if match else None

playlist_url = 'https://open.spotify.com/playlist/4tItRNUhmDBasg22H06mRu?si=af7b158d67224872' # my playlist
playlist_id = get_playlist_id(playlist_url)
playlist = sp.playlist(playlist_id)

nodes = []
edges = []

artist_genre_map = {}

for item in playlist['tracks']['items']: # this thing took wayy to long [mostly due to my own choices]
    track = item['track']
    track_name = track['name']
    track_id = track['id']
    track_node = {"id": track_id, "label": track_name, "type": "track"}
    nodes.append(track_node)

    for artist in track['artists']:
        artist_id = artist['id']
        artist_name = artist['name']
        artist_node = {"id": artist_id, "label": artist_name, "type": "artist"}

        # Avoid duplicates
        if not any(n['id'] == artist_id for n in nodes):
            nodes.append(artist_node)

        edges.append({"source": track_id, "target": artist_id, "relation": "created_by"})

        # Fetch genres if not already fetched
        if artist_id not in artist_genre_map:
            artist_info = sp.artist(artist_id)
            genres = artist_info['genres']
            artist_genre_map[artist_id] = genres

            for genre in genres:
                genre_id = f"genre_{genre}"
                genre_node = {"id": genre_id, "label": genre, "type": "genre"}
                if not any(n['id'] == genre_id for n in nodes):
                    nodes.append(genre_node)

                edges.append({"source": artist_id, "target": genre_id, "relation": "belongs_to"})

# Save to JSON
graph_data = {
    "nodes": nodes,
    "edges": edges
}

with open("spotify_playlist_graph.json", "w", encoding='utf-8') as f:
    json.dump(graph_data, f, indent=2)

print("spotify_playlist_graph.json created")
