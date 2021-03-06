# Spotify playlist creator module

from os import listdir
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from json import load as jload
import discogs_client

def public_private_check(playlist,spot,user_id,playlist_id,public_private_tag) -> None:
    """
    Checks that playlist is correct
    Changes playlist status if not correct
    """
    status = playlist['public']

    if status == public_private_tag:
        return
    else:
        spot.user_playlist_change_details(
            user_id,
            playlist_id,
            name=None,
            public=public_private_tag,
            collaborative=None,
            description=None)


def tracks_to_playlist(spot,user_id,playlist_id,track_ids: list) -> None:
    """
    add tracks to the new playlist
    """
    spot.user_playlist_add_tracks(
        user_id, 
        playlist_id, 
        track_ids, 
        position=None)


def create_playlist(spot,playlist_name: str,user_id,public_private_tag: str) -> str:
    """
    create a blank playlist with playlist_name
    """
    
    name = playlist_name
    description = input(
        "Please enter a discription of your new playlist and/or press enter")

    playlist = spot.user_playlist_create(
        user_id, 
        name, 
        public=public_private_tag, 
        collaborative=False, 
        description=description)
    
    playlist_id = playlist["id"]
    return(playlist_id,playlist)


def get_user_id(spot) -> str:
    """
    returns spotify user id
    """
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

        track_data = spot.search(q=track,limit=1,offset=0,type="track")
        number_returned = track_data['tracks']['total']

        if number_returned == int(0):
            print(f"{track}Not available")
        else:
            track_id = track_data['tracks']['items'][0]['id']
            track_artist = track_data['tracks']['items'][0]['artists'][0]['name']
            track_name = track_data['tracks']['items'][0]['name']
            print(track_name,track_artist, track_id)
            id_list.append(track_id)

    return(id_list)
    

def discog_search(disc: discogs_client.Client) -> list:
    """
    search Discog for user input info
    this is meant for adding albums to a playlist
    or for searching track by track
    """
    search = input("What are you searching for? \n1. Album \n2. Track \n \n")
    
    success: bool = False
    while not success:
        success = True

        match search:
            case "1":
                artist = input("Please enter artist name: ")
                album = input("Pleaase enter album name: ")
                track_data = disc.search(
                    type="master",
                    query=album,
                    artist=artist)

                track_list = []

                track_list_data = track_data[0].tracklist
                i = 0 
                for Track in track_list_data:
                    title = track_list_data[i].title
                    i = i + 1 
                    track_list.append(title + " " + artist)

                return track_list

            case "2":
                success: bool = False
                while not success:
                    success = True
                    track_list: list = []
                    enter_tracks = input("Finished? \n1. No \n2. Yes")

                    match enter_tracks:
                        case "1":
                            track = input("Please enter track name: ")
                            artist = input("Please enter artist name: ")
                            track_list.append(f"{track} {artist}")
                        case "2":
                            return track_list
                        case _:
                            success = False
            case _:
                success = False

        

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


def get_track_names(disc) -> list:
    """
    creates a track list from different input methods
    there are multiple methods of inputing a track list
    1. .txt file
    2. .JSON file
    3. .YML file 
    4. Search Discogs 
    """
    success: bool = False
    while not success:
        success = True

        method = input(
            "\n Please select an input method: \n1. File \n2. Search\n \n")

        match method:
            case "1":
                file_name: str = choose_playlist_file()
                return read_playlist(file_name)

            case "2":
                return discog_search(disc)

            case _:
                success = False
    

def choose_playlist_name() -> str:
    """
    user input a title for the playlist
    """
    playlist_title = input("please enter your playlist name: ")
    print(f"\nYour playlist title is: {playlist_title}")

    return playlist_title



def spotify_auth(scope: str) -> spotipy.Spotify:
    """
    create authentication token for Spotify
    """
    with open("./config.json", mode="r") as user_cred_file:
        user_cred = jload(user_cred_file)

    client_id: str = user_cred["SPOTIPY_CLIENT_ID"]
    client_secret: str = user_cred["SPOTIPY_CLIENT_SECRET"]
    redirect_uri: str = user_cred["SPOTIPY_REDIRECT_URI"]

    spot_oa = SpotifyOAuth(
        scope=scope, 
        client_id=client_id,
        client_secret=client_secret, 
        redirect_uri=redirect_uri)

    sp = spotipy.Spotify(auth_manager=spot_oa)

    return sp


def discog_auth() -> discogs_client.Client:
    """
    create authenication token for Discog
    """
    with open("./config.json", mode="r") as user_cred_file:
        user_cred = jload(user_cred_file)

    user_token: str = user_cred["DISCOG_USER_TOKEN"] 

    dc = discogs_client.Client(
        "SpotifyPlaylistGenerator/0.1", 
        user_token=user_token)

    return dc


def public_private() -> str:
    """ 
    allows user to choose between a public or private playlist
    """
    scope: str = "playlist-modify-public"
    public = input("Would you like this playlist to be public? y/n: ")
    match public:
        case "y":
            public_private_tag = True
        case "n":
            public_private_tag = False
            scope = f"{scope},playlist-modify-private"
    
    return scope, public_private_tag
