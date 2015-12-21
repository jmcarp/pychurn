# -*- coding: utf-8 -*-

import collections

import click
import tabulate

from version import get_churn

def format_change(change):
    parts = [change.file, change.name]
    if change.parent:
        parts.insert(1, change.parent)
    return ':'.join(parts)

@click.command()
@click.option('--path', default='.', type=click.Path())
@click.option('--since')
@click.option('--until')
def churn(path, since, until):
    changes = get_churn(path=path, since=since, until=until)
    counts = collections.Counter(changes)
    table = [
        (format_change(change), count)
        for change, count in counts.most_common(20)
    ]
    print(tabulate.tabulate(table, headers=('code', 'count')))

if __name__ == '__main__':
    churn()