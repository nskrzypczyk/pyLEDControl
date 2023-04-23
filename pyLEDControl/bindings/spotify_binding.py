#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyCurrentTrack():
    artist: str
    album_art_url: str
    track_name: str
    is_playing: bool
    progress: int

    def __init__(self, data: None | dict) -> None:
        if not data:
            self = None
        else:
            self.album_art_url = data['item']['album']['images'][0]['url']
            self.artist = data['item']['artists'][0]['name']
            if len(data['item']['artists']) > 1:
                artist = artist + ", " + data['item']['artists'][1]['name']
            self.is_playing = data["is_playing"]
            self.progress = data["progress_ms"]
            self.track_name = data['item']["name"]


class SpotifyBinding:
    def __init__(self) -> None:
        token = spotipy.util.prompt_for_user_token(
            settings.SPOTIFY.USERNAME.value,
            "user-read-email,user-read-private,user-library-read,user-read-playback-state,user-modify-playback-state,user-read-currently-playing",
            settings.SPOTIFY.CLIENT_ID.value,
            settings.SPOTIFY.CLIENT_SECRET.value,
            settings.SPOTIFY.REDIRECT_URL.value
        )

        self.spotify = spotipy.Spotify(auth=token, client_credentials_manager=SpotifyClientCredentials(
            client_id=settings.SPOTIFY.CLIENT_ID.value, client_secret=settings.SPOTIFY.CLIENT_SECRET.value,),)

    def get(self) -> any:
        return self.spotify.current_user_playing_track()
