#bongo
Bongo is a file server which we at [Steinwurf](http://steinwurf.com/) use for serving executables and presenting performance plots.

##Installation
If you haven't already, install the following requisites:

```
sudo apt-get install python python-pip fabric
```

Depending on whether you are planning to run bongo in a [testing](#testing) or [production](#production) environment you need to take different actions. The following will guide you through either direction.

###Testing
If you just want to try out bongo, or do some testing you need to do the following.

Init the submodules to get [Bootstrap](http://getbootstrap.com/).

```
git submodule init
git submodule update
```

Setup a virtual environment

```
sudo pip install virtualenvwrapper
```

Add the virtualenvwrapper functions and variables to your path

```
printf export WORKON_HOME=$HOME/.virtualenvs\n >> ~/.bashrc
printf source /usr/local/bin/virtualenvwrapper.sh\n >> ~/.bashrc
source ~/.bashrc
```

Create a virtual env

```
mkvirtualenv bongo
```

mkvirtualenv will automatically activate the virtualenv. If you need to activate it at a later point you can use the following command:

```
workon bongo
```

*For a full list of virtualenvwrappers function, click [here](http://virtualenvwrapper.readthedocs.org/en/latest/).*

To install the bongo requirements, run the following command (while having the virtualenv activated):

```
pip install -Ur requirements.txt
```

###Production

To use bongo in production, simply use the included fabric script like so:

```
fab setup
```

This will trigger the following fabric tasks. Note that fabric will ask you for the host, username and password, alternatively, you can specify these using ````:

0. **create_user**: Create a new user called bongo
* **clone**: Clone the bongo repository  on the specified production server to the folder ``/home/bongo/webapps/bongo``
* **init**: Init the newly cloned repository
* **install_requirements**: Create an virtual environment and install the requirements
* **setup_apache**: Setup an Apache server to serve the application and associated static files
* **deploy_static_files**: Deploy the static files

Furthermore the fabric script can be used for managing a few operations on the server. These include:

* **update**: pulls any new changes to the remote repository
* **start**: starts the apache service
* **stop**: stops the apache service
* **restart**: restarts the apache service
* **error_log**: cats the error log located at `` /var/log/apache2/error.log`` on the remote server.

##Adding files
When debugging, put the files in ``bongo/files/files``.

In production, you can either put the files in ``/home/bongo/webapps/bongo/files/files``, and subsequently run:
```
fab deploy_static_files
```
Alternatively, you can put the files directly in ``/var/www/bongo/static/files``.

##Todo

0. Enable password protection of certain files.
*. Use special bongo file templates the ``files`` directory to allow custom templates for files in certain locations.
