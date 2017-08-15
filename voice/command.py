from enum import Enum


class VoiceCommand(Enum):
    ALBUM = r'play song (.*)'
    ARTIST = r'play singer (.*)'
    SHOW_ARTIST = r'show me some singers'
    SHOW_ALBUM = r'show me some songs'
    HELP = r'help'

    @staticmethod
    def print_voice_command():
        print("Available voice command:")
        for cmd in VoiceCommand:
            print('    {}'.format(cmd.value))