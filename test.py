from flask import Flask


app = Flask(__name__)

@app.route('/test')
def test():
    return 'Testing 123'

