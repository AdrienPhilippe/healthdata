#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Error(Exception):
    pass

class ValueNotFound(Error):
    pass

class DestNotSpecified(Error):
    pass

class WrongPasswordOrUsername(Error):
    pass

class RessourceAlreadyExists(Error):
    pass

class RessourceDoesNotExist(Error):
    pass