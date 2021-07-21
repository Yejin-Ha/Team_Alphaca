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
    chart, all_genre = get_new_chart()
    print('Load data from ES')
    return render_template('index.html', singer=singer, song=songs, chart=chart, all_genre=all_genre)


if __name__ == '__main__':
    app.run(debug=True)
