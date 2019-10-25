from player import *
import logging
import os
from  subprocess import Popen, threading
from kivy.core.window import Window
import time
import globals
from  pymediainfo import MediaInfo


"""
This is the media player we use for isha pi project.
On Raspberri PI we will be using the openmx player.
On virtual machines and testing on windows we can use mpv player
"""
class Player():
    exec = None
    supportedPlayers = {}
    process = None
    screensaver = None
    screenManager = None
    isPlaying = False

    def onPlayEnd(self):
        return

    def _playWorkThread(self):
        self.isPlaying = True
        while self.process.poll() == None:
            time.sleep(1)
        self.isPlaying = False
        self.onPlayEnd()


    def play(self, path):
        logging.info("Player: start playing file... path = {}".format(path))

        if not os.path.isfile(path):
            logging.error("Player: file not found")
            return

        mediaInfo = MediaInfo.parse(path)

        videoWidth, videoHeight = 0, 0
        for track in mediaInfo.tracks:
            if track.track_type == 'Video':
                videoWidth, videoHeight = track.width, track.height

        osdHeight = 50
        playerHeight = Window.height - (2*osdHeight)#videoHeight - osdHeight
        playerWidth = int(playerHeight * (videoWidth / videoHeight))


        posx = int((Window.width - playerWidth) / 2)
        posy = int((Window.height - playerHeight) / 2)

        logging.error("Player: playerWidth: {} / playerHeight: {} / videoWidth: {} / videoHeight: {} / posx: {} / posy: {}".format(
            playerWidth, playerHeight, videoWidth, videoHeight, posx, posy))



        self.isPlaying = True
        self.process = Popen([self.supportedPlayers[os.name],
                        "--geometry={}+{}+{}".format(playerWidth, posx, posy),
                        #"--geometry=1244+98+0",
                        "--no-border",
                        "--no-input-default-bindings",
                        path,
                        #"--really-quiet",
                        #"--no-osc",
                        "--ontop",
                        "--input-ipc-server={}".format(os.path.join(globals.config[os.name]['tmpdir'],"socket"))

                        ])

        self.playThread = threading.Thread(target = self._playWorkThread)
        self.playThread.setDaemon(True)
        self.playThread.start()
#"--really-quiet",
#"--no-osc",

# "--input-ipc-server={}".format(os.path.join(globals.config[os.name]['tmpdir'], "ishapiSocket")


    def __init__(self):#, screenManager, screenSaver):
        self.supportedPlayers['nt'] = "mpv.exe"
        self.supportedPlayers['posix'] = "mpv"
