from datetime import date
from flask import Flask, request, render_template, jsonify, redirect
from dao import *

app = Flask(__name__)

# home 화면
@app.route('/', methods=['get'])
def index():
    print('Open index page')
    singer = h_singer()
    songs = h_song()
    print('Load data from ES')
    return render_template('index.html', singer=singer, song=songs)


if __name__ == '__main__':
    app.run(debug=True)
