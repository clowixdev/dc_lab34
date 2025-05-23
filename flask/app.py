from flask import (Flask, 
                    render_template, 
                    request)
from os import environ
import requests

app = Flask(__name__)
app.secret_key = environ.get("FKEY")

@app.route('/')
def view_form():
    return render_template('index.html')

@app.route('/post', methods=['GET', 'POST'])
def handle_post():
    if request.method == 'POST':
        print(request.data)
        requests.post("http://127.0.0.1:8443", json=request.data)

    return "sent an answer"

if __name__ == '__main__':
    app.run(debug=False, 
            port=8443,
            ssl_context="adhoc")