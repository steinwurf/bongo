bongo
=====

File Server


Installation
============
First off we need pyhton and pip.

  $ apt-get install python python-pip

Now we need some tools which allows us to create an isolated python environment so that the requirements of bongo can be installed in isolation.

  $ pip install virtualenv
  $ pip install virtualenvwrapper

Note, we could just use virtualenv, but virtualenvwrapper makes this easier to work with.

Now you need to configure virtualenvwrapper add the follwoing to your shell startup file (e.g., .bash_profile).

  export WORKON_HOME=$HOME/.virtualenvs
  source /usr/local/bin/virtualenvwrapper.sh

You may need to reload the startup script before you can continue with this guide. Now create the bongo environment and install the requirements.

  mkvirtualenv bongo
  pip install -Ur requirements.txt

When you create the environment you will automatically activate it. To later deactivate run the following command:

  deactivate

When you want to reactivate run the following

  workon bongo

To see the full list of commands supported by virtualenvwrapper, go here: http://virtualenvwrapper.readthedocs.org/en/latest/command_ref.html

