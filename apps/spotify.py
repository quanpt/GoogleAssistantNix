# Copyright (C) 2017 Tran Quan Pham
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging as l
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
l.basicConfig(level=l.DEBUG, format=FORMAT)


import spotipy


# database & constants
client_id = '67292b56265946c1963408a7bcb5fffa'
client_secret = 'c5af3d371927415eb88d48778efb5035'
redirect_uri = 'http://localhost:8888/callback'
scopes = 'user-read-private user-read-email'


import sys
import spotipy
import spotipy.util as util

def show_tracks(tracks):
    for i, item in enumerate(tracks['items']):
        track = item['track']
        print("   %d %32.32s %s" % (i, track['artists'][0]['name'],
                              track['name']))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        username = sys.argv[1]
    else:
        print("Whoops, need your username!")
        print("usage: python user_playlists.py [username]")
        sys.exit()

    token = util.prompt_for_user_token(username)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:
                print
                print
                playlist['name']
                print
                '  total tracks', playlist['tracks']['total']
                results = sp.user_playlist(username, playlist['id'],
                                           fields="tracks,next")
                tracks = results['tracks']
                show_tracks(tracks)
                while tracks['next']:
                    tracks = sp.next(tracks)
                    show_tracks(tracks)
    else:
        print
        "Can't get token for", username
