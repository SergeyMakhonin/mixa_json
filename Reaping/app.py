from flask import Flask, request
from logging_and_configuration import log


app = Flask(__name__)





if __name__ == '__main__':
    # starting main server
    log('Starting main server...')
    app.run(debug=False)
