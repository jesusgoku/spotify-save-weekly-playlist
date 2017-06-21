#!/usr/bin/env python

from __future__ import print_function, unicode_literals

import sys

from datetime import date, timedelta

import spotipy
import spotipy.util as util


def track_id(track_object):
    return track_object['track']['id']


def get_first_date_of_week():
    today = date.today()
    return today - timedelta(days=today.weekday())


if __name__ == '__main__':
    scope = 'user-library-read playlist-modify-private'

    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Usage: {} username".format(sys.argv[0]))
        sys.exit()

    token = util.prompt_for_user_token(username, scope)

    if token:
        sp = spotipy.Spotify(auth=token)

        first_day_of_week = get_first_date_of_week()

        discover_weekly_pl = sp.user_playlist(
            'spotify',
            '37i9dQZEVXcTNgtrEFg1QP')

        tracks_id = map(track_id, discover_weekly_pl['tracks']['items'])

        weekly_playlist = sp.user_playlist_create(
            username,
            'Lista Semanal {}'.format(first_day_of_week.strftime('%Y%m%d')),
            False)

        sp.user_playlist_add_tracks(
            username,
            weekly_playlist['id'],
            map(track_id, discover_weekly_pl['tracks']['items']))
    else:
        print("Can't get token for", username)
