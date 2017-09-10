#!/usr/bin/env python
import pygame
import time
from mutagen.mp3 import MP3
from src.se_manager import play
from src.util import getColorString
from src.util import getColorText


def status(args):
    args.se_manager.play_wav("pi")
    args.state.use_mp(1)
    if args.state.add_exp(10):
        return "level up!", False
    return "", False
