# -*- coding: utf-8 -*-

import fnmatch

def match(path, patterns):
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)

def check_path(path, include=(), exclude=()):
    return (
        (not include or match(path, include)) and
        not match(path, exclude)
    )
