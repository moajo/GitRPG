#!/usr/bin/env python

import sys
from typing import List
from datetime import datetime
import pickle
import os

import time

from src.util import getColorText

state_path = os.path.dirname(__file__) + "/../state"


class State:
    def __init__(self, lv, max_mp, mp, max_hp, hp):
        self.hp = hp
        self.max_hp = max_hp
        self.mp = mp
        self.max_mp = max_mp
        self.lv = lv
        self.combo = []
        self.last_command_time = int(time.mktime(datetime.now().timetuple()))

    def __repr__(self):
        return f"lv:{self.lv}\nmax_mp: {self.max_mp}\n max_hp: {self.max_hp}"

    # コマンドを実行したことを通知、コンボ用。
    def command(self, command):
        now = int(time.mktime(datetime.now().timetuple()))
        delta = now - self.last_command_time
        self.last_command_time = now
        if delta < 5:
            self.combo.append(command)
        else:
            self.reset_combo()

    def reset_combo(self):
        self.combo = []

    def lv_up(self, hp_delta, mp_delta):
        self.max_hp += hp_delta
        self.max_mp += mp_delta
        self.hp = self.max_hp
        self.mp = self.max_mp
        self.lv += 1
        self.save()

    def use_mp(self, amount):
        self.mp -= amount
        self.save()

    def damage(self, amount):
        self.hp -= amount
        self.save()

    def normalize(self):
        if self.hp < 0:
            self.hp = 0
        if self.mp < 0:
            self.mp = 0
            self.save()

    def showStr(self):
        if float(self.hp / self.max_hp) <= 0.1:
            return f"LV: {self.lv} HP:" + getColorText("{0}/{1}".format(self.hp, self.max_hp),
                                                       91) + f" MP: {self.mp}/{self.max_mp}"
        elif float(self.hp / self.max_hp) <= 0.3:
            return f"LV: {self.lv} HP:" + getColorText("{0}/{1}".format(self.hp, self.max_hp),
                                                       93) + f" MP: {self.mp}/{self.max_mp}"
        else:
            return f"LV: {self.lv} HP: {self.hp}/{self.max_hp} MP: {self.mp}/{self.max_mp}"

    def save(self):
        with open(state_path + '/state.pickle', 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def initial_state():
        return State(1, 10, 10, 10, 10)


def load_state():
    if not os.path.exists(state_path):
        os.mkdir(state_path)
    if not os.path.exists(f"{state_path}/state.pickle"):
        return State.initial_state()

    with open(state_path + '/state.pickle', 'rb') as f:
        return pickle.load(f)
