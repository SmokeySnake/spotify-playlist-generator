
from itertools import count
from os import listdir, read
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from json import load as jload
import discogs_client

# Take a list of track names in a text file
# and use this to cxreate a Spotify playlist

def tracks_to_playlist(spot,user_id,playlist_id,track_ids: list) -> None:
    """
    add tracks to the new playlist
    """
    spot.user_playlist_add_tracks(user_id, playlist_id, track_ids, position=None)


def create_playlist(spot,playlist_name: str,user_id) -> str:
    """
    create a blank playlist
    """
    name = playlist_name
    description = input("Please enter a discription of your new playlist or just press enter")

    public = input("Would you like this playlist to be public? y/n: ")
    if public == "y":
        public =  True 
    elif public == "n":
        public =  False

    playlist = spot.user_playlist_create(user_id, name, public, collaborative=False, description=description)
    
    playlist_id = playlist["id"]
    return(playlist_id)


def get_user_id(spot) -> str:
    user_info = spot.me()
    user_id = user_info["id"]

    return(user_id)


def get_track_ids(spot: spotipy.Spotify, track_names: list) -> list:
    """
    search for each song name on Spotify
    parse song meta data for the song id 
    put each song id into a list
    """
    id_list = []
    for track in track_names:
    #     #search spotify
        track_data = spot.search(q=track,limit=1,offset=0,type="track")
        track_id = track_data['tracks']['items'][0]['id']
        track_artist = track_data['tracks']['items'][0]['artists'][0]['name']
        track_name = track_data['tracks']['items'][0]['name']
        print(track_name,track_artist, track_id)
        id_list.append(track_id)

    return(id_list)
    

def read_playlist(playlist_file: str) -> list:
    """
    create a list to add track ids
    take each line in the file of track names
    """
    playlist = "./playlists/" + playlist_file
    print(playlist)
    
    with open(playlist,'r') as file:
        tracks = file.readlines()
    return (tracks)


def choose_playlist_file() -> str:
    """
    prints a list of files in the playlist directory
    user chooses file from this list using the numeretical value of 
    the chosen playlists placement in the list
    """

    playlists: list = sorted(listdir("./playlists"))
    print(f"Please chhose a playlist from the list:")

    for i, title in enumerate(playlists):
        print(f"{i}: {title}")

    selection: int = int(input())

    return playlists[selection]


def track_list() :
    """
    creates a track list from different input methods
    there are multiple methods of inputing a track list
    1. .txt file
    2. .JSON file
    3. .YML file 
    4. Search Discogs 
    """

    method = input("\n \n Please select an input method: \n1. File \n2. Search")
    if method == 1:
        choose_playlist_file()
    elif method == 2:
        track_list_search 
    


def choose_playlist_name() -> str:
    """
    user input a title for the playlist
    """
    playlist_title = input("please enter your playlist name: ")
    print(f"\nYour playlist title is: {playlist_title}")

    return playlist_title


def login() -> spotipy.Spotify:
    """
    create authentication token for Spotify
    """
    with open("./config.json", mode="r") as user_cred_file:
        user_cred = jload(user_cred_file)

    client_id: str = user_cred["SPOTIPY_CLIENT_ID"]
    client_secret: str = user_cred["SPOTIPY_CLIENT_SECRET"]
    redirect_uri: str = user_cred["SPOTIPY_REDIRECT_URI"]

    scope = "playlist-modify-private"

    spot_oa = SpotifyOAuth(scope=scope, client_id=client_id,
                           client_secret=client_secret, redirect_uri=redirect_uri)
    sp = spotipy.Spotify(auth_manager=spot_oa)

    return sp

def discog_auth() -> discogs_client.Client:
    """
    create authenication token for Discog
    """
    with open("./config.json", mode="r") as user_cred_file:
        user_cred = jload(user_cred_file)

    user_token: str = user_cred["DISCOG_USER_TOKEN"] 

    dc = discogs_client.Client("SpotifyPlaylistGenerator/0.1", user_token=user_token)

    return dc


def main() -> None:
    print("\n Welcome to Spotify Playlist Generator! ", end="\n \n")

    disc: discogs_client.Client = discog_auth()

    spot: spotipy.Spotify = login()

    playlist_name: str = choose_playlist_name()

    file_name: str = choose_playlist_file()

    track_names: list = read_playlist(file_name)

    track_ids: list = get_track_ids(spot, track_names)

    user_id: str = get_user_id(spot)

    playlist_id = create_playlist(spot, playlist_name,user_id)

    tracks_to_playlist(spot,user_id,playlist_id,track_ids)


if __name__ == '__main__':
    main() 
