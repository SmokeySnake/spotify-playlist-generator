
from os import listdir, read
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from json import load as jload

# Take a list of song names in a text file
# and use this to cxreate a Spotify playlist


def create_playlist(playlist_name: str, id_list: list) -> None:
    """
    use song ids list to create a playlist 
    in spotify
    """


def get_song_ids(spot: spotipy.Spotify, songnames: list) -> list:
    """
    search for each song name
    get the song id
    """


def read_playlist(playlist_file: str) -> list:
    """
    create a list to add song ids
    take each line in the file of song names
    """
    id_list: list = []


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


def choose_playlist_name() -> str:
    """
    user input a title for the playlist
    """

    playlist_title = input("please enter your playlist name: ")
    print(f"\nYour playlist title is: {playlist_title}")


def login() -> spotipy.Spotify:
    with open("./config.json", mode="r") as user_cred_file:
        user_cred = jload(user_cred_file)

    client_id: str = user_cred["SPOTIPY_CLIENT_ID"]
    client_secret: str = user_cred["SPOTIPY_CLIENT_SECRET"]
    redirect_uri: str = user_cred["SPOTIPY_REDIRECT_URI"]

    scope = "user-library-read"

    spot_oa = SpotifyOAuth(scope=scope, client_id=client_id,
                           client_secret=client_secret, redirect_uri=redirect_uri)
    sp = spotipy.Spotify(auth_manager=spot_oa)

    return sp


def main() -> None:
    print("\n Welcome to Spotify Playlist Generator! ", end="\n \n")

    spot: spotipy.Spotify = login()

    playlist_name: str = choose_playlist_name()

    file_name: str = choose_playlist_file()

    song_names: list = read_playlist(file_name)

    song_ids: list = get_song_ids(spot, song_names)

    create_playlist(spot, playlist_name, song_ids)


if __name__ == '__main__':
    main() 
