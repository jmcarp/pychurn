# -*- coding: utf-8 -*-

import re
import ast
import itertools
import collections

import git

from parse import ChurnVisitor

pattern = re.compile(r'(?P<op>[+-])(?P<start>\d+)(?:,(?P<count>\d+))? @@')

def parse_diff_lines(diff):
    for line in diff.diff.decode().splitlines():
        if not line.startswith('@@'):
            continue
        match = pattern.search(line)
        if match:
            params = match.groupdict()
            start, count = int(params['start']), int(params['count'] or 1)
            yield range(start, start + count)

def parse_diff(diff):
    return set(itertools.chain.from_iterable(parse_diff_lines(diff)))

Change = collections.namedtuple('Change', ['file', 'type', 'name', 'parent'])

def get_churn(path, since=None, until=None):
    repo = git.Repo(path)
    opts = {
        'min_parents': 1,
        'max_parents': 1,
        'since': since,
        'until': until,
    }
    opts = {key: value for key, value in opts.items() if value is not None}
    for commit in repo.iter_commits(**opts):
        diffs = commit.parents[0].diff(commit, create_patch=True, unified=0)
        for diff in diffs:
            changes = parse_diff(diff)
            try:
                source = repo.git.show('{}:{}'.format(commit.hexsha, diff.b_path))
            except (git.GitCommandError, UnicodeDecodeError):
                continue
            try:
                parsed = ast.parse(source)
            except SyntaxError:
                continue
            for node in ChurnVisitor.extract(parsed):
                if changes.intersection(range(node.lineno, node.lineno_end)):
                    yield Change(
                        diff.b_path,
                        type(node),
                        node.name,
                        node.parent.name if node.parent else None,
                    )
