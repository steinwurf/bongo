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
        env.installer = prompt('What is your package handling utility.',
                               default = 'aptitude')

def install(package):
    setup_installer()
    env.sudo('{0} install {1}'.format(env.installer, package))

@task
def remote(git_top_level, bongoPort):
    env.bongoPort     = bongoPort
    env.local         = False
    env.debug         = False
    env.git_top_level = git_top_level

    env.run           = rrun
    env.cd            = rcd
    env.exists        = rexists
    env.sudo          = rsudo

@task
def local(debug = 'True', git_top_level = None, bongoPort = 8080):
    env.bongoPort     = bongoPort
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
    install_requirements()
    setup_apache()
    deploy_static_files()

@task
def clone():
    if env.debug:
        print "No need to clone, you already have done that."
        return

    env.run('mkdir -p {}'.format(env.git_top_level))
    install('git')
    env.run('git clone https://github.com/steinwurf/bongo.git {0}'.format(
        env.git_top_level))

@task
def init():
    with env.cd(env.git_top_level):
        env.run('git submodule init')
        env.run('git submodule update')

@task
def install_requirements():
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
    if env.debug:
        print('No need to install apache as this is only for debugging.')
        return
    install('apache2')
    install('libapache2-mod-wsgi')
    env.sudo('a2dissite default')
    override = True
    apacheFile = '/etc/apache2/sites-available/bongo'
    if env.exists(apacheFile):
        override = confirm('Do you want to override the file'
            '"{}"?'.format(apacheFile))
        if override:
            env.sudo('rm {}'.format(apacheFile))

    if override:
        env.sudo('printf "{0}" >> {1}'.format(
            ('<VirtualHost *:80>\n'
            '    ServerName 127.0.1.1\n'
            '    WSGIDaemonProcess bongo-production user={user} group=bongo '
                    'threads=10 python-path=/home/{user}/.virtualenvs/bongo'
                    '/lib/python2.7/site-packages\n'
            '    WSGIProcessGroup bongo-production\n'
            '    WSGIScriptAlias / {git_top_level}/bongo/bongo.wsgi\n'
            '    Alias /static/ /var/wwww/bongo/static/\n'
            '    <Directory {git_top_level}/bongo>\n'
            '        Order deny,allow\n'
            '        Allow from all\n'
            '    </Directory>\n'
            '    ErrorLog /var/log/apache2/error.log\n'
            '    LogLevel warn\n'
            '    CustomLog /var/log/apache2/access.log combined\n'
            '</VirtualHost>').format(**{
                    'bongoPort'      : env.bongoPort,
                    'user'          : env.user,
                    'git_top_level' : env.git_top_level
                }),
            apacheFile
            ))
        with env.cd('/etc/apache2/sites-enabled'):
            if env.exists('bongo'):
                env.sudo('rm bongo')
            env.sudo('ln -s ../sites-available/bongo')

    restart()

@task
def deploy_static_files():
    env.sudo('mkdir -p /var/wwww/bongo/static/')
    with env.cd(env.git_top_level):
        with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
            with prefix('workon bongo'):
                env.sudo('./manage.py collectstatic')


@task
def start():
    if not env.debug:
        env.run('/etc/init.d/apache2 start')
    else:
        print('Run "./manage runserver 8080" in the console')
@task
def stop():
    if not env.debug:
        env.run('/etc/init.d/apache2 stop')

@task
def restart():
    if not env.debug:
        env.sudo('/etc/init.d/apache2 restart')
    else:
        stop()
        start()
@task
def update(git_top_level = None):
    with env.cd(env.git_top_level):
        env.run('git pull')

@task
def clone_bongo(project_location = ''):
    if project_location == '':
        project_location = project_name
    if env.exists(project_location):
        print("'{}' already exists.".format(project_location))
        return
    env.run('git clone https://github.com/steinwurf/bongo.git {0}'.format(
        project_location))