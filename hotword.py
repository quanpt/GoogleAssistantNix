#!/usr/bin/env python

# Copyright (C) 2017 Google Inc.
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


from __future__ import print_function

import argparse
import os.path
import json

import google.oauth2.credentials

from google.assistant.library import Assistant
from google.assistant.library.event import EventType
from google.assistant.library.file_helpers import existing_file

from apps import kodi
from sound import amixer
from voice import command

import logging as l

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
l.basicConfig(level=l.ERROR, format=FORMAT)


def process_event(event, assistant):
    """Pretty prints events.

    Prints all events that occur with two spaces between each new
    conversation and a single space between turns of a conversation.

    Args:
        event(event.Event): The current event to process.
    """
    if event.type == EventType.ON_CONVERSATION_TURN_STARTED:
        print("Listening ...")
        amixer.set_low_sound_level()

    l.info(event)

    if event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
        amixer.restore_sound_level()
        spokenText = event.args['text']
        print("Command: {}".format(spokenText))
        if kodi.is_valid_command(spokenText):
            print("  executing  ")
            kodi.execute_command()
            assistant.stop_conversation()
        else:
            print("  use Google Assistant")

    if (event.type == EventType.ON_CONVERSATION_TURN_FINISHED and
            event.args and not event.args['with_follow_on_turn']):
        print('Done')


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--credentials', type=existing_file,
                        metavar='OAUTH2_CREDENTIALS_FILE',
                        default=os.path.join(
                            os.path.expanduser('~/.config'),
                            'google-oauthlib-tool',
                            'credentials.json'
                        ),
                        help='Path to store and read OAuth2 credentials')
    args = parser.parse_args()
    with open(args.credentials, 'r') as f:
        credentials = google.oauth2.credentials.Credentials(token=None,
                                                            **json.load(f))

    with Assistant(credentials) as assistant:
        assistant.set_mic_mute(False)
        kodi.init_database()
        command.VoiceCommand.print_voice_command()
        for event in assistant.start():
            process_event(event, assistant)


if __name__ == '__main__':
    main()
