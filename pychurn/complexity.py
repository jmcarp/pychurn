# -*- coding: utf-8 -*-

import os
import types

import git
import radon.complexity

from pychurn import utils

def get_complexity(path, include=(), exclude=()):
    repo = git.Repo(path)
    for _, blob in repo.index.iter_blobs():
        if not utils.check_path(blob.name, include, exclude):
            continue
        with open(os.path.join(path, blob.path)) as fp:
            source = fp.read()
        try:
            visitor = radon.complexity.ComplexityVisitor.from_code(source)
        except (SyntaxError):
            continue
        for node in visitor.classes:
            yield ((blob.path, type, node.name, None), node.complexity)
            for child in visitor.functions:
                yield ((blob.path, types.MethodType, child.name, node.name), child.complexity)
        for node in visitor.functions:
            yield ((blob.path, types.FunctionType, node.name, None), node.complexity)
