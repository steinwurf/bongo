from fabric.api import task
from fabric.api import run as rrun
from fabric.api import cd as rcd
from fabric.api import sudo as rsudo
from fabric.colors import red
from fabric.context_managers import lcd, prefix
from fabric.contrib.console import confirm, prompt
from fabric.contrib.files import exists as rexists
from fabric.operations import local as lrun
from fabric.operations import require
from fabric.state import env
from os.path import exists as lexists
from distutils.util import strtobool
import os

env.hosts = ["192.168.6.82"]
env.user = "bongo"

def setup_installer():
    if 'installer' not in env:
        env.installer = prompt('What is the remote package handling utility',
                               default = 'aptitude')

def install(package):
    setup_installer()
    env.sudo('{0} install {1}'.format(env.installer, package))

@task
def remote(git_top_level):
    env.local         = False
    env.debug         = False
    env.git_top_level = git_top_level

    env.run           = rrun
    env.cd            = rcd
    env.exists        = rexists
    env.sudo          = rsudo

@task
def local(debug = 'True', git_top_level = None):
    env.debug = bool(strtobool(debug))
    env.local = True
    if env.debug:
        env.git_top_level = os.path.dirname(os.path.realpath(__file__))
    elif git_top_level:
        env.git_top_level = git_top_level
    else:
        print(red('You must specify a git top level if you are not running in'
                  'debug mode.', True))
        exit(1)

    env.run    = lambda cmd : lrun(cmd, shell='/bin/bash')
    env.cd     = lcd
    env.exists = lexists
    env.sudo   = lambda cmd : env.run('sudo {}'.format(cmd))

@task
def setup():
    require('local', provided_by=[local, remote])
    clone()
    init()
    if confirm('Do you want this script to setup the bongo requirements? '
               'python, pip, django, and virtualenvwrapper will be '
               'installed and configured.'):
        install_requirements()
    setup_apache()
    deploy_static_files()

@task
def clone():
    require('local', provided_by=[local, remote])
    if env.debug:
        print "No need to clone, you already have done that."
        return

    env.run('mkdir -p {}'.format(env.git_top_level))
    install('git')
    env.run('git clone https://github.com/steinwurf/bongo.git {0}'.format(
        env.git_top_level))

@task
def init():
    require('local', provided_by=[local, remote])
    with env.cd(env.git_top_level):
        env.run('git submodule init')
        env.run('git submodule update')

@task
def install_requirements():
    require('local', provided_by=[local, remote])
    install('python')
    install('python-pip')

    env.sudo('pip install virtualenvwrapper')

    env.run('printf "{}" >> ~/.bashrc'.format(
            'export WORKON_HOME=$HOME/.virtualenvs\n'
            'source /usr/local/bin/virtualenvwrapper.sh\n'))

    env.run('export WORKON_HOME=$HOME/.virtualenvs')

    with env.cd(env.git_top_level):
        with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
            env.run('mkvirtualenv bongo')
            with prefix('workon bongo'):
                env.run('pip install -Ur requirements.txt')

@task
def setup_apache():
    require('local', provided_by=[local, remote])
    if env.debug:
        print('No need to install apache as this is only for production.')
        return
    install('apache2')
    install('libapache2-mod-wsgi')
    env.sudo('a2dissite default')

    apache_file = '/etc/apache2/sites-available/bongo'
    if env.exists(apache_file):
        env.sudo('rm {}'.format(apache_file))

    secret_key = prompt(
        'Please provide the django secret key', default='testing')
    with env.cd(os.path.join(git_top_level, 'bongo'):
        env.run('rm -f SECRET')
        env.run('echo {} >> SECRET'.format(secret_key))

    env.sudo('printf "{0}" >> {1}'.format(
       ('<VirtualHost *:80>\n'
        '    ServerName 127.0.1.1\n'
        '    WSGIDaemonProcess bongo-production user={user} group=bongo '
                'threads=10 python-path=/home/{user}/.virtualenvs/bongo'
                '/lib/python2.7/site-packages\n'
        '    WSGIProcessGroup bongo-production\n'
        '    WSGIScriptAlias / {git_top_level}/bongo/wsgi.py\n'
        '    Alias /static/ /var/www/bongo/static/\n'
        '    <Directory {git_top_level}/bongo>\n'
        '        Order deny,allow\n'
        '        Allow from all\n'
        '    </Directory>\n'
        '    ErrorLog /var/log/apache2/error.log\n'
        '    LogLevel warn\n'
        '    CustomLog /var/log/apache2/access.log combined\n'
        '</VirtualHost>\n').format(**env), apache_file))
    with env.cd('/etc/apache2/sites-enabled'):
        if env.exists('bongo'):
            env.sudo('rm bongo')
        env.sudo('ln -s ../sites-available/bongo')

    restart()

@task
def deploy_static_files():
    require('local', provided_by=[local, remote])
    if env.debug:
        print('No need to deploy static files as this is only for production.')
        return
    env.sudo('mkdir -p /var/www/bongo/static/')
    with env.cd(env.git_top_level):
        with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
            with prefix('workon bongo'):
                env.sudo('./manage.py collectstatic -v0 --noinput')

@task
def start():
    require('local', provided_by=[local, remote])
    if not env.debug:
        env.run('/etc/init.d/apache2 start')
    else:
        print('Run "./manage runserver 8080" in the console')
@task
def stop():
    require('local', provided_by=[local, remote])
    if not env.debug:
        env.run('/etc/init.d/apache2 stop')

@task
def restart():
    require('local', provided_by=[local, remote])
    if not env.debug:
        env.sudo('/etc/init.d/apache2 restart')
    else:
        stop()
        start()
@task
def update(git_top_level = None):
    require('local', provided_by=[local, remote])
    with env.cd(env.git_top_level):
        env.run('git pull')
