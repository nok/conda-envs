#!/usr/bin/env python
# -*- coding: utf-8 -*-

# <bitbar.title>Anaconda Environments</bitbar.title>
# <bitbar.author>Darius Morawiec</bitbar.author>
# <bitbar.author.github>nok</bitbar.author.github>
# <bitbar.desc>Open a Terminal with a specific conda environment.</bitbar.desc>


import os
import subprocess


CONDA_PATH = '~/anaconda/bin/conda'


class Color:
    GREEN = '#3bb15c'
    BLUE = '#4a90f3'
    WHITE = '#ffffff'


class Env:
    def __init__(self, env_name):
        conda = os.path.expanduser(CONDA_PATH)
        cmd = [conda, 'env', 'export', '-n', env_name]
        deps = subprocess.check_output(cmd, stderr=subprocess.STDOUT).strip()

        version = None
        for dep in deps.splitlines():
            if '- python=' in dep:
                version = dep.split('=')[1]
                env_name += ' (%s)' % version
                break

        self.env_name = env_name
        self.version = version

    @property
    def color(self):
        if self.version is None:
            return Color.WHITE
        else:
            major = self.version.split('.')[0]
            if major is '2':
                return Color.GREEN
        return Color.BLUE

    def __str__(self):
        return ('%s | color=%s bash=source param1=activate '
                'param2=%s terminal=true refresh=false') % (
               self.env_name, self.color, self.env_name)


def main():
    conda = os.path.expanduser(CONDA_PATH)

    cmd = [conda, 'env', 'list']
    envs = subprocess.check_output(cmd, stderr=subprocess.STDOUT).strip()

    menu = []
    for env in envs.splitlines():
        if not env.strip().startswith('#'):
            tuple = env.split()
            name, path = tuple[0], tuple[1]
            if any(['*', 'root']) not in tuple:
                menu.append(Env(name))

    print('𝗔')
    if len(menu) > 0:
        print('---')
        for env in menu:
            print(env)
        print('---')
        print('Python 2 | color=%s' % Color.GREEN)
        print('Python 3 | color=%s' % Color.BLUE)
        print('---')

    cmd = [conda, '--version']
    ver = subprocess.check_output(cmd, stderr=subprocess.STDOUT).strip()
    print(ver)


if __name__ == "__main__":
    main()
