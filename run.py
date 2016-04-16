#!flask/bin/python
from app import app
from socket import gethostname

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
                app.run("localhost", 5000, debug=True)
