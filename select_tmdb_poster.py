#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Description:  Selects the default TMDB poster if no poster is selected
              or the current poster is from Gracenote.
Author:       /u/SwiftPanda16
Requires:     plexapi
Usage:
    * Change the posters for an entire library:
        python select_tmdb_poster.py --library "Movies" --poster

    * Change the art for an entire library:
        python select_tmdb_poster.py --library "Movies" --art

    * Change the posters and art for an entire library:
        python select_tmdb_poster.py --library "Movies" --poster --art

    * Change the poster for a specific item:
        python select_tmdb_poster.py --rating_key 1234 --poster

    * Change the art for a specific item:
        python select_tmdb_poster.py --rating_key 1234 --art

    * Change the poster and art for a specific item:
        python select_tmdb_poster.py --rating_key 1234 --poster --art

    * By default locked posters are skipped. To update locked posters:
        python select_tmdb_poster.py --library "Movies" --include_locked --poster --art

    * To override the preferred provider:
        python select_tmdb_poster.py --library "Movies" --art --art_provider "fanarttv"

Tautulli script trigger:
    * Notify on recently added
Tautulli script conditions:
    * Filter which media to select the poster. Examples:
        [ Media Type | is | movie ]
Tautulli script arguments:
    * Recently Added:
        --rating_key {rating_key} --poster --art
'''

import argparse
import os
import plexapi.base
from plexapi.server import PlexServer
plexapi.base.USER_DONT_RELOAD_FOR_KEYS.add('fields')


# Poster and art providers to replace
REPLACE_PROVIDERS = ['gracenote', 'plex', None]

# Preferred poster and art provider to use (Note not all providers are available for all items)
# Possible options: tmdb, tvdb, imdb, fanarttv, gracenote, plex
PREFERRED_POSTER_PROVIDER = 'tmdb'
PREFERRED_ART_PROVIDER = 'tmdb'


# ## CONFIG ##
# Prefer passing secrets via environment variables or CLI args.
# Example:
#   export PLEX_URL='http://127.0.0.1:32400'
#   export PLEX_TOKEN='YOUR_TOKEN'

DEFAULT_PLEX_URL = 'http://127.0.0.1:32400'
PLEX_URL = os.getenv('PLEX_URL', DEFAULT_PLEX_URL)
PLEX_TOKEN = os.getenv('PLEX_TOKEN', '')


def select_library(
    library,
    include_locked=False,
    poster=False,
    poster_provider=PREFERRED_POSTER_PROVIDER,
    art=False,
    art_provider=PREFERRED_ART_PROVIDER
):
    for item in library.all(includeGuids=False):
        # Only reload for fields
        item.reload(**{k: 0 for k, v in item._INCLUDES.items()})
        select_item(
            item,
            include_locked=include_locked,
            poster=poster,
            poster_provider=poster_provider,
            art=art,
            art_provider=art_provider
        )


def select_item(
    item,
    include_locked=False,
    poster=False,
    poster_provider=PREFERRED_POSTER_PROVIDER,
    art=False,
    art_provider=PREFERRED_ART_PROVIDER
):
    print(f"{item.title} ({item.year})")

    if poster:
        select_poster(item, include_locked, poster_provider)
    if art:
        select_art(item, include_locked, art_provider)


def select_poster(item, include_locked=False, provider=PREFERRED_POSTER_PROVIDER):
    _select_image(item, 'poster', 'thumb', include_locked, provider)


def select_art(item, include_locked=False, provider=PREFERRED_ART_PROVIDER):
    _select_image(item, 'art', 'art', include_locked, provider)


def _select_image(item, kind, lock_tag, include_locked, provider):
    print(f"  Checking {kind}...")

    if item.isLocked(lock_tag) and not include_locked:  # PlexAPI 4.5.10
        print(f"  - Locked {kind} for {item.title}. Skipping.")
        return

    # Dynamically call .posters() or .arts() based on kind
    images = getattr(item, kind + 's')()
    selected_image = next((p for p in images if p.selected), None)

    if selected_image is None:
        print(f"  - WARNING: No {kind} selected for {item.title}.")
    else:
        skipping = ' Skipping.' if selected_image.provider not in REPLACE_PROVIDERS else ''
        print(f"  - {kind.capitalize()} provider is '{selected_image.provider}' for {item.title}.{skipping}")

    if images and (selected_image is None or selected_image.provider in REPLACE_PROVIDERS):
        # Fallback to first image if no preferred provider images are available
        provider_image = next((p for p in images if p.provider == provider), images[0])
        # Selecting the image automatically locks it
        provider_image.select()
        print(f"  - Selected {provider_image.provider} {kind} for {item.title}.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rating_key', type=int)
    parser.add_argument('--library')
    parser.add_argument('--include_locked', action='store_true')
    parser.add_argument('--poster', action='store_true')
    parser.add_argument('--poster_provider', default=PREFERRED_POSTER_PROVIDER)
    parser.add_argument('--art', action='store_true')
    parser.add_argument('--art_provider', default=PREFERRED_ART_PROVIDER)

    # Optional overrides
    parser.add_argument('--plex_url', default=None)
    parser.add_argument('--plex_token', default=None)

    opts = parser.parse_args()

    plex_url = opts.plex_url or PLEX_URL
    plex_token = opts.plex_token or PLEX_TOKEN

    if not plex_token:
        raise SystemExit(
            "PLEX_TOKEN is not set. Set env var PLEX_TOKEN or pass --plex_token."
        )

    plex = PlexServer(plex_url, plex_token)

    if opts.rating_key:
        item = plex.fetchItem(opts.rating_key)
        select_item(item, opts.include_locked, opts.poster, opts.poster_provider, opts.art, opts.art_provider)
    elif opts.library:
        library = plex.library.section(opts.library)
        select_library(library, opts.include_locked, opts.poster, opts.poster_provider, opts.art, opts.art_provider)
    else:
        print("No --rating_key or --library specified. Exiting.")
