# Sample Python code for user authorization

import httplib2
import json
from apps import kodi

from apiclient.discovery import build
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import logging as l
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
l.basicConfig(level=l.INFO, format=FORMAT)

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "./google_client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"

_range = 5
_shownAlbum = []


# Authorize the request and store authorization credentials.
def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READ_WRITE_SSL_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("youtube-api-snippets-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    # Trusted testers can download this discovery document from the developers page
    # and it should be in the same directory with the code.
    return build(API_SERVICE_NAME, API_VERSION,
                 http=credentials.authorize(httplib2.Http()))


def print_results(results):
    print(json.dumps(results, indent=4, sort_keys=True))


# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        for key in kwargs.keys():
            value = kwargs[key]
            if value:
                good_kwargs[key] = value
    return good_kwargs


# Sample python code for search.list
def search_list_by_keyword(service, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)  # See full sample for function
    results = service.search().list(
        **kwargs
    ).execute()
    return results


def search_play_album(label):
    service = get_authenticated_service(None)
    results = search_list_by_keyword(service,
                           part='snippet',
                           maxResults=1,
                           q=label,
                           type='playlist')
    item = results['items'][0]
    l.info(item)
    play_album((item['id']['playlistId'], item['snippet']['title']))


def search_play_song(label):
    service = get_authenticated_service(None)
    results = search_list_by_keyword(service,
                           part='snippet',
                           maxResults=1,
                           q=label,
                           type='video')
    item = results['items'][0]
    l.info(item)
    play_song((item['id']['videoId'], item['snippet']['title']))


def show_albums(label):
    global _shownAlbum
    service = get_authenticated_service(None)
    results = search_list_by_keyword(service,
                                     part='snippet',
                                     maxResults=_range,
                                     q=label,
                                     type='video')
    _shownAlbum = [(item['id']['videoId'], item['snippet']['title']) for item in results['items']]
    print('\n'.join(['    {}. {}'.format(str(index + 1), _shownAlbum[index][1]) for index in range(_range)]))


def play_album(video_item):
    l.info(video_item)
    kodi.play_youtube_album(video_item[0])


def play_song(video_item):
    l.info(video_item)
    kodi.play_youtube_song(video_item[0])


def main():
    search_play_song('katy perry roar')

if __name__ == '__main__':
    main()