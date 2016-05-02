import os
import types
import shutil
import datetime
import tempfile
import textwrap

import git
import pytest

from pychurn import utils
from pychurn import version

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
        os.environ['GIT_AUTHOR_DATE'] = str(datetime.datetime(2016, 1, idx + 1))
        os.environ['GIT_COMMITTER_DATE'] = str(datetime.datetime(2016, 1, idx + 1))
        repo.index.add([mod])
        repo.index.commit('update module {}'.format(idx))
    try:
        yield repo
    finally:
        shutil.rmtree(path)

def test_churn(repo):
    nodes = list(version.get_churn(repo.working_dir))
    expected = [
        utils.Node(file='module.py', type=types.FunctionType, name='func', parent=None),
        utils.Node(file='module.py', type=type, name='Klass', parent=None),
        utils.Node(file='module.py', type=type, name='Klass', parent=None),
        utils.Node(file='module.py', type=types.MethodType, name='meth', parent='Klass'),
    ]
    assert nodes == expected

def test_churn_since_sha(repo):
    commits = list(repo.iter_commits())
    nodes = list(version.get_churn(repo.working_dir, since=commits[0].committed_date))
    expected = [
        utils.Node(file='module.py', type=types.FunctionType, name='func', parent=None),
        utils.Node(file='module.py', type=type, name='Klass', parent=None),
    ]
    assert nodes == expected
