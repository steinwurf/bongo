bongo
=====

File Server


Installation
============
First off, we need to install pyhton, pip, and fabric on the server which is to host bongo.::

  $ apt-get install python python-pip fabric

Now we need a tool called virtualenvwrapper. This allows us to create an isolated python environment so that the requirements of bongo can be contained.::

  $ pip install virtualenvwrapper

Note, virtualenvwrapper is, as the name may imply, just a wrapper for virtualenv that makes it easier to work with.

Now you need to configure virtualenvwrapper. Add the follwoing to your shell startup file (e.g., ``.bashrc``)::

  export WORKON_HOME=$HOME/.virtualenvs
  source /usr/local/bin/virtualenvwrapper.sh

You need to reload the startup script (reboot or do a ``source [startup file]``, e.g., ``.bashrc``) before you can continue with this guide.

Now you are ready to utilize the fabric script to easily get bongo up and running. The fabric script can be used in three scenarios,

#. Run bongo locally in a debug environment (fab localhost debug [command]).
#. Run bongo locally in a environment (fab localhost [command]).
#. Run bongo remotely in a environment (fab remote [command]).

Now use fabric to create the bongo environment and install the requirements::

  fab localhost install_requirements

