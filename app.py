from flask import Flask, request, render_template, send_file, make_response, current_app
from flask_cors import CORS
import requests
import functions

# %% Flask app
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def isAlive():
    return "It is working"

@app.route('/vote', methods=['GET'])
def vote():
    id_post = request.args.get("id")
    response_post = request.args.get("response")
    response = functions.addVote(id_post,response_post)
    return str(response)

@app.route('/data', methods=['GET'])
def obtain_data():
    return str(functions.readPickle())

if __name__ == '__main__':
    app.run()