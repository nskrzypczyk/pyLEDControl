#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import spotipy

import settings


# RUN THIS SCRIPT ON DESKTOP AND COPY TO FILE TO THE RESPECTIVE PATH

username = sys.argv[1]
scope = "user-read-currently-playing"

auth = spotipy.SpotifyOAuth(
    client_id=settings.SPOTIFY.CLIENT_ID.value,
    client_secret=settings.SPOTIFY.CLIENT_SECRET.value,
    username=settings.SPOTIFY.USERNAME.value,
    redirect_uri=settings.SPOTIFY.AUTH_URL.value,
    scope=scope,
    open_browser=False,
)
token = auth.get_access_token()
