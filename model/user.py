#! -*- coding: utf-8 -*-

from brome.core.model.stateful import Stateful

class User(Stateful):

    def __init__(self, pdriver, username, password):
        self.pdriver = pdriver
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User: username: %s>"%self.username
