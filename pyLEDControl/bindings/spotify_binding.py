#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import settings
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyBinding:
    def __init__(self) -> None:
        self.spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                settings.SPOTIFY.CLIENT_ID.value, settings.SPOTIFY.CLIENT_SECRET.value
            )
        )

    def get(self) -> any:
        return self.spotify.current_user_playing_track()
