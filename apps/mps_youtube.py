import logging as l
import time
import subprocess, os

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
l.basicConfig(level=l.WARN, format=FORMAT)

def search_play_song(track):
    l.info(track)

    pkill = subprocess.Popen(["/usr/bin/pkill","vlc"],stdin=subprocess.PIPE)

    FNULL = open(os.devnull, 'w')
    playshell = subprocess.Popen(["mpsyt",""],stdin=subprocess.PIPE, stdout=FNULL, stderr=subprocess.STDOUT)# ,stdout=subprocess.PIPE)

    playshell.stdin.write(bytes('/' + track + '\n1\nq\n', 'utf-8'))
    playshell.stdin.flush()

    # while True:
    #     line = playshell.stdout.readline()
    #     if line == b'':
    #         break

    # pkill = subprocess.Popen(["/usr/bin/pkill","vlc"],stdin=subprocess.PIPE)


def main():
    search_play_song('katy perry roar')

if __name__ == '__main__':
    main()