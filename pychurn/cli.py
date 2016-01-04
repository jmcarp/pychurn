# -*- coding: utf-8 -*-

import collections

import click
import tabulate

from pychurn.version import get_churn
from pychurn.complexity import get_complexity

def format_change(change):
    parts = [change.file, change.name]
    if change.parent:
        parts.insert(1, change.parent)
    return ':'.join(parts)

@click.group()
def cli():
    pass

@cli.command()
@click.option('--path', default='.', type=click.Path())
@click.option('--include', multiple=True)
@click.option('--exclude', multiple=True)
@click.option('--since')
@click.option('--until')
def churn(**kwargs):
    changes = get_churn(**kwargs)
    counts = collections.Counter(changes)
    table = [
        (format_change(change), count)
        for change, count in counts.most_common(20)
    ]
    print(tabulate.tabulate(table, headers=('code', 'count')))

@cli.command()
@click.option('--path', default='.', type=click.Path())
@click.option('--include', multiple=True)
@click.option('--exclude', multiple=True)
@click.option('--until')
def complexity(**kwargs):
    results = sorted(
        get_complexity(**kwargs),
        key=lambda pair: pair[1],
        reverse=True,
    )
    table = [
        (format_change(change), value)
        for change, value in results[:20]
    ]
    print(tabulate.tabulate(table, headers=('code', 'complexity')))

@cli.command()
@click.option('--path', default='.', type=click.Path())
@click.option('--sort', default='churn', type=click.Choice(['churn', 'complexity']))
@click.option('--count', default=20, type=click.INT)
@click.option('--include', multiple=True)
@click.option('--exclude', multiple=True)
@click.option('--since')
@click.option('--until')
def report(**kwargs):
    sort, count, since = kwargs.pop('sort'), kwargs.pop('count'), kwargs.pop('since')
    changes = get_churn(since=since, **kwargs)
    counts = collections.Counter(changes)
    scores = dict(get_complexity(**kwargs))
    keys = set(counts.keys()) | set(scores.keys())
    merged = sorted(
        [
            (key, counts.get(key, 0), scores.get(key, 0))
            for key in keys
        ],
        key=lambda triple: triple[1 if sort == 'churn' else 2],
        reverse=True,
    )
    table = [
        (format_change(change), churn, complexity)
        for change, churn, complexity in merged[:count]
    ]
    print(tabulate.tabulate(table, headers=('code', 'churn', 'complexity')))
