from datetime import date
from flask import Flask, request, render_template, jsonify, redirect
from dao import *

app = Flask(__name__)

# home 화면
@app.route('/', methods=['get'])
def index():
    print('Open index page')
    hot_song, oldest_result, hot_singer = get_hot()
    chart, all_genre = get_new_chart()
    print('Load data from ES')
    return render_template('index.html', singer=hot_singer, oldest=oldest_result, song=hot_song, chart=chart, all_genre=all_genre)


if __name__ == '__main__':
    app.run(debug=True)
