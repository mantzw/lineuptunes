import requests
import base64
import urllib.parse
import os

def lineuptunes_lambda_handler(event, context):
    """
    AWS lambda python application that will be used to help create spotify playlists that contain the artist lineups for music festivals.
    """
    
    playlist_name = event["playlist_name"] + " - Unofficial"
    auth_code = event["auth_code"]
    number_of_songs_to_add = event["number_of_songs_to_add"]
    artist_list = event["artist_list"]


    # Get Access Token
    client_id = os.environ['CLIENT_ID']
    client_secret = os.environ['CLIENT_SECRET']

    auth_url = "https://accounts.spotify.com/api/token"

    # Create the authorization header
    auth_value = f"{client_id}:{client_secret}"
    auth_header = {
        'Authorization': 'Basic ' + base64.b64encode(auth_value.encode('utf-8')).decode('utf-8'),
        'Content-Type': "application/x-www-form-urlencoded"
    }

    auth_data = {
        "code": f"{auth_code}",
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:9000/callback"
    }
    auth_response = requests.post(auth_url, headers=auth_header, data=auth_data)
    print("AUTH RESPONSE", auth_response.status_code, auth_response.json())

    access_token = auth_response.json()["access_token"]

    basic_auth_header = {
        'Authorization': "Bearer " + access_token,
    }
    basic_post_headers = {
        'Authorization': "Bearer " + access_token,
        'Content-Type': 'application/json'
    }

    # Get user Id
    get_user_url = "https://api.spotify.com/v1/me"
    get_user_response = requests.get(url=get_user_url, headers=basic_auth_header)

    user_id = get_user_response.json()["id"]

    # Create playlist
    create_playlist_url = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    create_playlist_data = {
        "name": playlist_name,
        "description": playlist_name,
        "public": True
    }
    create_playlist_response = requests.post(url=create_playlist_url, headers=basic_post_headers, json=create_playlist_data)

    playlist_id = create_playlist_response.json()["id"]
    print("PLAYLIST ID:", playlist_id)

    search_base_url = 'https://api.spotify.com/v1/search'
    bad_search = []
    for artist in artist_list:
        # SEARCH for artist
        query = f"artist:{artist}"
        encoded_search_query = urllib.parse.quote(query)
        search_url = f"{search_base_url}?q={encoded_search_query}&type=artist"

        search_response = requests.get(url=search_url, headers=basic_auth_header)
        if search_response.status_code > 200:
            bad_search.append(artist)

        searched_artist = search_response.json()["artists"]
        if len(searched_artist["items"]) > 0:
            artist_id = searched_artist["items"][0]["id"]
        else:
            bad_search(artist)

        # GET top artist tracks
        top_tracks_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks"
        top_tracks_response = requests.get(url=top_tracks_url, headers=basic_auth_header)

        top_tracks = top_tracks_response.json()["tracks"]
        song_ids_to_add = []
        for i in range(0, number_of_songs_to_add):
            if i < len(top_tracks):
                song_ids_to_add.append("spotify:track:" + top_tracks[i]["id"])

        # ADD tracks to playlist
        add_items_to_playlist_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        add_items_to_playlist_data = {
            "uris": song_ids_to_add
        }

        requests.post(url=add_items_to_playlist_url, headers=basic_post_headers, json=add_items_to_playlist_data)

    if len(bad_search) > 0:
        print("Bad artist search:", bad_search)