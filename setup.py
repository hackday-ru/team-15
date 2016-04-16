#!/usr/bin/python
import os, subprocess, sys
subprocess.call(['python3', 'virtualenv.py', 'flask'])
if sys.platform == 'win32':
    bin = 'Scripts'
else:
    bin = 'bin'
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'flask<0.10'])
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'flask-login'])
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'flask-openid'])
if sys.platform == 'win32':
    subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', '--no-deps', 'lamson', 'chardet', 'flask-mail'])
else:
    subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'flask-mail'])
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'sqlalchemy==0.7.9'])
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'flask-sqlalchemy'])
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'sqlalchemy-migrate'])
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'flask-whooshalchemy'])
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'flask-wtf'])
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'flask-babel'])
subprocess.call([os.path.join('flask', bin, 'pip3'), 'install', 'flup'])
