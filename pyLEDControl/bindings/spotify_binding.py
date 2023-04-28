#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyCurrentTrack:
    artist: str
    album_art_url: str
    track_name: str
    is_playing: bool
    progress: int
    track_length_ms: int
    track_length_s: float
    track_length_min: float

    def __init__(self, data: None) -> None:
        if not data:
            self = None
        else:
            self.album_art_url = data["item"]["album"]["images"][0]["url"]
            self.artist = data["item"]["artists"][0]["name"]
            if len(data["item"]["artists"]) > 1:
                self.artist = self.artist + ", " + data["item"]["artists"][1]["name"]
            self.is_playing = data["is_playing"]
            self.progress = data["progress_ms"]
            self.track_name = data["item"]["name"]
            self.track_length_ms = data["item"]["duration_ms"]
            self.track_length_s = self.track_length_ms / 1000
            self.track_length_s = round(self.track_length_s / 60, 2)


class SpotifyBinding:
    def __init__(self) -> None:
        cache_handler = spotipy.CacheFileHandler(settings.SPOTIFY.CACHE_PATH.value)
        self.spotify = spotipy.Spotify(
            auth_manager=spotipy.SpotifyOAuth(
                client_id=settings.SPOTIFY.CLIENT_ID.value,
                client_secret=settings.SPOTIFY.CLIENT_SECRET.value,
                redirect_uri=settings.SPOTIFY.REDIRECT_URL.value,
                cache_handler=cache_handler,
            )
        )

    def get(self) -> SpotifyCurrentTrack:
        return SpotifyCurrentTrack(self.spotify.current_user_playing_track())
