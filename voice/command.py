from enum import Enum
import re

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

    @staticmethod
    def extract_data(spoken_text):
        search_param_1 = None
        for cmd in VoiceCommand:
            match = re.search(cmd.value, spoken_text, flags=re.IGNORECASE)
            if match:
                if cmd in [VoiceCommand.ARTIST, VoiceCommand.ALBUM]:
                    search_param_1 = match.group(1).lower()
                return (cmd, search_param_1)
        return (None, None)