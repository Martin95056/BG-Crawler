from db_creator import session
from models import Server
from flask import Flask, render_template, jsonify
import json

with open('end_servers_histogram.json', 'w') as f:
    data = json.load(f)

app = Flask(__name__)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/results')
def show_results():
    return jsonify(data)


@app.route('/histogram')
def show_histogram():
    return render_template('show_histogram.html')


@app.route('/thug')
def thug_life():
    return render_template('thug.html')


@app.route('/results/<platform_name>')
def get_result_for_platform(platform_name):
    result = session.query(Server).\
              filter(Server.platform == platform_name).first()

    return str(result.quntity)

if __name__ == '__main__':
    app.run(debug=True)
