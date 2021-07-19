from flask import Flask, request, render_template, jsonify, redirect


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
    # Flask 로 실행하기 위한 필수 코드
    # debug = True : 서버가 실행중이더라도 소스 수정 -> 자동 갱신이 가능
    app.run(debug=True)
