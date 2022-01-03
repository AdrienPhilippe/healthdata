#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Error(Exception):
    pass

class ValueNotFound(Error):
    pass

class DestNotSpecified(Error):
    pass