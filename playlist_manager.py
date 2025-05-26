import json
import os

PLAYLIST_FILE = "playlists.json"

# make sure file exists
if not os.path.exists(PLAYLIST_FILE):
    with open(PLAYLIST_FILE, "w") as f:
        json.dump({}, f)

def load_playlists():
    with open(PLAYLIST_FILE, "r") as f:
        return json.load(f)

def save_playlists(playlists):
    with open(PLAYLIST_FILE, "w") as f:
        json.dump(playlists, f, indent=4)

def create_playlist(server_id, name):
    playlists = load_playlists()
    server_id = str(server_id)

    if server_id not in playlists:
        playlists[server_id] = {}

    if name in playlists[server_id]:
        return False  # Playlist already exists

    playlists[server_id][name] = []
    save_playlists(playlists)
    return True

def add_to_playlist(server_id, name, song_info):
    playlists = load_playlists()
    server_id = str(server_id)

    if server_id not in playlists or name not in playlists[server_id]:
        return False

    playlists[server_id][name].append(song_info)
    save_playlists(playlists)
    return True

def get_playlist(server_id, name):
    playlists = load_playlists()
    server_id = str(server_id)

    return playlists.get(server_id, {}).get(name)