from spotify_playlist_creator_module import *

# Take a list of track names in a text file
# or searches discogs for an album track list
# and use this to create a Spotify playlist


def main() -> None:
    print("\n Welcome to Spotify Playlist Generator! ", end="\n \n")

    scope, public_private_tag = public_private()

    disc: discogs_client.Client = discog_auth()

    spot: spotipy.Spotify = spotify_auth(scope)

    playlist_name: str = choose_playlist_name()

    track_names: list = get_track_names(disc)

    track_ids: list = get_track_ids(spot, track_names)

    user_id: str = get_user_id(spot)

    playlist_id, playlist = create_playlist(spot, playlist_name,user_id,public_private_tag)

    tracks_to_playlist(spot,user_id,playlist_id,track_ids)

    public_private_check(playlist,spot,user_id,playlist_id,public_private_tag)

    print("\nCongratulations! \n\nYour playlist has been created!")


if __name__ == '__main__':
    main() 
