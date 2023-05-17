from flask import Flask
server = Flask(__name__)

@server.route('/')
def hello_world():
    return '/'

@server.route('/env')
def print_env():
    import os
    print(os.environ)
    return '/env'

if __name__ == "__main__":
    server.run(host='0.0.0.0', port=8000)