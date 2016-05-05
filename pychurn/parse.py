# -*- coding: utf-8 -*-

import ast

class ChurnVisitor(ast.NodeVisitor):

    def __init__(self):
        self.nodes = []

    def visit_FunctionDef(self, node, parent=None):
        self.report(node, parent=parent)

    def visit_ClassDef(self, node):
        self.report(node)
        for child in node.body:
            if isinstance(child, ast.FunctionDef):
                self.visit_FunctionDef(child, parent=node)

    def report(self, node, parent=None):
        node.parent = parent
        node.lineno_end = get_lineno_end(node)
        self.nodes.append(node)

    @classmethod
    def extract(cls, node):
        instance = cls()
        instance.visit(node)
        return instance.nodes

def get_lineno_end(node):
    return max(
        child.lineno
        for child in iter_terminal(node)
        if hasattr(child, 'lineno')
    )

def iter_terminal(node):
    children = list(ast.iter_child_nodes(node))
    if children:
        yield children[-1]
        for grandchild in iter_terminal(children[-1]):
            yield grandchild
