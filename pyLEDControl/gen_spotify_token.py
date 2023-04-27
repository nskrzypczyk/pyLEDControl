#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import spotipy

import settings


# RUN THIS SCRIPT ON DESKTOP AND COPY TO FILE TO THE RESPECTIVE PATH

username = sys.argv[1]
scope = "user-read-currently-playing"


spotipy.util.prompt_for_user_token(
    client_id=settings.SPOTIFY.CLIENT_ID.value,
    client_secret=settings.SPOTIFY.CLIENT_SECRET.value,
    username=settings.SPOTIFY.USERNAME.value,
    redirect_uri=settings.SPOTIFY.REDIRECT_URL.value,
    scope=scope,
)
