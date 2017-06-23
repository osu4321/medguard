# MEDGuard
The most amazing application for all things medical.  No warranty - does not actually provide any medical benefit.

# About
This is a project by MACMed Software for InfoSec Summer 17.

## Version
alpha-0.1

## Local Install

The following are instructions for local install on a Debian based linux.  I enjoy Linux Mint.

1. Create a new local directory.
2. Initialize a new local git repo. `git init`
3. Pull from this remote repo: `git pull https://github.com/osu4321/medguard`
4. Create your Python 3.5 virtual environment
* 'pyvenv-3.5 env' "env" is the folder where the virtual environment has been installed
* activate the venv with `source env/bin/activate`
5. Install project dependencies. `pip3 install -r requirements.txt`
6. Run app from project directory. `python3 run.py`