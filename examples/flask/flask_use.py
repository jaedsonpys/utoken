from flask import Flask, request
from flask import make_response
from flask import render_template
from flask import redirect, url_for
from flask import jsonify

import utoken

app = Flask(__name__, template_folder='templates')
UTOKEN_KEY = 'KEY'


@app.route('/')
def index():
    token = request.cookies.get('utoken')

    if not token:
        return redirect(url_for('register'))

    try:
        decode_utoken = utoken.decode(token, UTOKEN_KEY)
    except (utoken.InvalidTokenError, utoken.InvalidContentTokenError):
        return redirect(url_for('register'))

    return jsonify(you=decode_utoken)


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        data['by'] = 'Firlast'

        user_token = utoken.encode(data, UTOKEN_KEY)
        response = make_response(redirect(url_for('index')))
        response.set_cookie('utoken', user_token)

        return response

    return render_template('register.html')


if __name__ == '__main__':
    app.run(port=3030, debug=True)
