from flask import Flask, request, render_template, jsonify, redirect
from dao import bank_get2

app = Flask(__name__)

# home 화면
@app.route('/', methods=['get'])
def index():
    print('Open index page')
    return render_template('index.html')


# @app.route('/getfilm',methods=['POST'])
# def getFilm():
#     dao = Camera()
#     return dao.allFilms()


if __name__ == '__main__':
    app.run(debug=True)
