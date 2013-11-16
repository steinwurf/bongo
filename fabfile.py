from fabric.api import task
from fabric.api import run
from fabric.api import cd
from fabric.api import sudo
from fabric.colors import red
from fabric.context_managers import lcd, prefix
from fabric.contrib.console import confirm, prompt
from fabric.contrib.files import exists
from fabric.operations import require
from fabric.state import env
import os

GIT_TOP_LEVEL = '/home/bongo/webapps/bongo'

def install(package):
    if 'installer' not in env:
        prompt('What is the remote package handling utility', key = 'installer',
                               default = 'aptitude')
    sudo('{0} install {1}'.format(env.installer, package))

@task
def setup():
    create_user()
    clone()
    init()
    install_requirements()
    setup_apache()
    deploy_static_files()

@task
def create_user():
    # Hacky way of seeing whether the bongo user exists
    if 'bongo' in run('ls /home'):
        print("bongo user already seem to exist, not creating one.")
    else:
        password = prompt('Write the desired password for the bongo user:')
        sudo('useradd -m -U bongo')
        sudo("echo -e '{0}\n{0}\n' | sudo passwd bongo".format(password))

@task
def clone():
    if not exists(GIT_TOP_LEVEL):
        sudo('mkdir -p {}'.format(GIT_TOP_LEVEL), 'bongo')
        install('git')
        sudo('git clone https://github.com/steinwurf/bongo.git {0}'.format(
            GIT_TOP_LEVEL), 'bongo')

@task
def init():
    with cd(GIT_TOP_LEVEL):
        sudo('git submodule init', 'bongo')
        sudo('git submodule update', 'bongo')

@task
def install_requirements():
    install('python')
    install('python-pip')

    sudo('pip install virtualenvwrapper')

    if confirm('Do you wish to add the virtualenvwrapper variables to '
               '~/.bashrc?', False):
        sudo('printf "{}" >> /home/bongo/.bashrc'.format(
            'export WORKON_HOME=$HOME/.virtualenvs\n'
            'source /usr/local/bin/virtualenvwrapper.sh\n'), 'bongo')

    with cd(GIT_TOP_LEVEL):
        with prefix('export HOME=/home/bongo'):
            with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
                sudo('mkvirtualenv bongo', 'bongo')
                with prefix('workon bongo'):
                    sudo('pip install -Ur requirements.txt', 'bongo')

@task
def setup_apache():
    install('apache2')
    install('libapache2-mod-wsgi')
    #Disable the default page
    sudo('a2dissite default')
    #Enable wsgi mod
    sudo('a2enmod wsgi')

    apache_file = '/etc/apache2/sites-available/bongo'
    if exists(apache_file):
        sudo('rm {}'.format(apache_file))

    secret_key = prompt(
        'Please provide a secret key for django', default='testing')
    with cd(os.path.join(GIT_TOP_LEVEL, 'bongo')):
        sudo('rm -f SECRET', 'bongo')
        sudo('echo {} >> SECRET'.format(secret_key), 'bongo')

    sudo('printf "{0}" >> {1}'.format(
       ('<VirtualHost *:80>\n'
        '    ServerName 127.0.1.1\n'
        '    WSGIDaemonProcess bongo-production user=bongo group=bongo '
                'threads=10 python-path=/home/bongo/.virtualenvs/bongo'
                '/lib/python2.7/site-packages\n'
        '    WSGIProcessGroup bongo-production\n'
        '    WSGIScriptAlias / {0}/bongo/wsgi.py\n'
        '    Alias /static/ /var/www/bongo/static/\n'
        '    <Directory {0}/bongo>\n'
        '        Order deny,allow\n'
        '        Allow from all\n'
        '    </Directory>\n'
        '    ErrorLog /var/log/apache2/error.log\n'
        '    LogLevel warn\n'
        '    CustomLog /var/log/apache2/access.log combined\n'
        '</VirtualHost>\n').format(GIT_TOP_LEVEL), apache_file))
    with cd('/etc/apache2/sites-enabled'):
        sudo('rm -f bongo')
        sudo('ln -s ../sites-available/bongo')

    restart()

@task
def deploy_static_files():
    sudo('mkdir -p /var/www/bongo/static/')
    with cd(GIT_TOP_LEVEL):
        with prefix('export HOME=/home/bongo'):
            with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
                with prefix('workon bongo'):
                    sudo('./manage.py collectstatic -v0 --noinput', 'bongo')

@task
def start():
    sudo('/etc/init.d/apache2 start')

@task
def stop():
    sudo('/etc/init.d/apache2 stop')

@task
def restart():
    sudo('/etc/init.d/apache2 restart')

@task
def update():
    with cd(GIT_TOP_LEVEL):
        sudo('git pull', 'bongo')

@task
def error_log():
    run('cat /var/log/apache2/error.log')