import os
import time
import types
import shutil
import datetime
import tempfile
import textwrap

import git
import pytest

from pychurn import parse
from pychurn.gitsource.pygitsource import PyGitSource
from pychurn.gitsource.libgitsource import LibGitSource

versions = [
    '''
    def func():
        print('func')

    class Klass():
        class_var = 'class_var'
        def meth(self):
            print('meth')
    ''',
    '''
    def func():
        print('func')

    class Klass():
        class_var = 'class_var'
        def meth(self):
            print('meth changed')
    ''',
    '''
    def func():
        print('func changed')

    class Klass():
        class_var = 'class_var_changed'
        def meth(self):
            print('meth changed')
    '''
]

@pytest.yield_fixture
def repo():
    path = tempfile.mkdtemp()
    repo = git.Repo.init(path)
    for idx, source in enumerate(versions):
        mod = os.path.join(repo.working_dir, 'module.py')
        with open(mod, 'w') as fp:
            fp.write(textwrap.dedent(source))
        date = datetime.datetime(2016, 1, idx + 1).isoformat()
        os.environ['GIT_AUTHOR_DATE'] = date
        os.environ['GIT_COMMITTER_DATE'] = date
        repo.index.add([mod])
        repo.index.commit('update module {}'.format(idx))
    try:
        yield repo
    finally:
        shutil.rmtree(path)

@pytest.mark.parametrize(['klass'], [
    (PyGitSource, ),
    (LibGitSource, ),
])
def test_churn(klass, repo):
    nodes = list(klass(repo.working_dir).churn())
    expected = [
        parse.Node(file='module.py', type=types.FunctionType, name='func', parent=None),
        parse.Node(file='module.py', type=type, name='Klass', parent=None),
        parse.Node(file='module.py', type=type, name='Klass', parent=None),
        parse.Node(file='module.py', type=types.MethodType, name='meth', parent='Klass'),
    ]
    assert nodes == expected

@pytest.mark.parametrize(['klass'], [
    (PyGitSource, ),
    (LibGitSource, ),
])
def test_churn_since_date(klass, repo):
    commits = list(repo.iter_commits())
    since = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(commits[1].committed_date))
    nodes = list(klass(repo.working_dir, since=since).churn())
    expected = [
        parse.Node(file='module.py', type=types.FunctionType, name='func', parent=None),
        parse.Node(file='module.py', type=type, name='Klass', parent=None),
    ]
    assert nodes == expected
