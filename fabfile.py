from fabric.api import task
from fabric.api import run as rrun
from fabric.api import cd as rcd
from fabric.api import sudo as rsudo
from fabric.colors import red
from fabric.context_managers import lcd, prefix
from fabric.contrib.console import confirm, prompt
from fabric.contrib.files import exists as rexists
from fabric.operations import local as lrun
from fabric.state import env
from os.path import exists as lexists
from distutils.util import strtobool
import os

env.hosts = ["192.168.6.82"]
env.user = "demo1"

def setup_installer():
    if 'installer' not in env:
        env.installer = prompt('What is your package handling utility.',
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
    clone()
    init()
    install_requirements()
    setup_apache()

@task
def clone():
    if env.debug:
        print "No need to clone, you already have done that."
        return
    if env.exists(env.git_top_level):
        print("'{}' already exists.".format(env.git_top_level))
        return
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
            env.run('mkvirtualenv bongo_test')
            with prefix('workon bongo_test'):
                env.run('pip install -Ur requirements.txt')

@task
def setup_apache():
    if env.debug:
        print('No need to install apache as this is only for debugging.')
        return
    install('apache2')
    install('libapache2-mod-wsgi')

    override = True
    apacheFile = '/etc/apache2/site-available/bongo'
    if env.exists(apacheFile):
        override = confirm('Do you want to override the file'
            '"{}"?'.format(apacheFile))

    if override:
        env.sudo('echo {0} >> {1}'.format(
            '<VirtualHost *:80>'
            '    ServerName bongo'
            '    WSGIDaemonProcess bongo-production user=bongo group=bongo threads=10 python-path=/home/bongo/.virtualenvs/bongo/lib/python2.7/site-packages'
            '    WSGIProcessGroup bongo-production'
            '    WSGIScriptAlias / {0}/deploy/bongo.wsgi'
            '    <Directory {0}/deploy>'
            '        Order deny,allow'
            '        Allow from all'
            '    </Directory>'
            '    ErrorLog /var/log/apache2/error.log'
            '    LogLevel warn'
            '    CustomLog /var/log/apache2/access.log combined'
            '</VirtualHost>'.format(env.git_top_level),
            apacheFile
            ))
        with env.cd('/etc/apache2/sites-enabled'):
            env.run('ln -s ../sites-available/bongo')

    env.run('/etc/init.d/apache2 restart')

    # apache2 setup
    if not env.is_production:
        print "No need for git clone, as this is only when running production."


@task
def start():
    pass
@task
def stop():
    pass

@task
def restart():
    pass

@task
def update(git_top_level = None):
    if not git_top_level:
        git_top_level = os.path.dirname(os.path.realpath(__file__))

    print "update"

@task
def production_install(project_location = ''):
    clone_bongo(project_location)
    init_bongo(project_location)
    install_bongo('')
    #install_requirements('')

@task
def clone_bongo(project_location = ''):
    if project_location == '':
        project_location = project_name
    if env.exists(project_location):
        print("'{}' already exists.".format(project_location))
        return
    env.run('git clone https://github.com/steinwurf/bongo.git {0}'.format(
        project_location))



# @task
# def install_requirements(project_location = ''):
#     if project_location == '':
#         project_location = project_name
#     if confirm('Install and setup virtualenvwrapper?', True):
#         env.sudo('apt-get install python-pip')
#         env.sudo('pip install virtualenvwrapper')
#     with env.cd(project_location):

@task
def deploy(project_location = ''):
    if project_location == '':
        project_location = project_name

    with env.cd(project_location):
        env.run('git pull')
        env.run('workon {}'.format(project_name))