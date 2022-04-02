from flask import Flask
from flask import request,jsonify

app = Flask("abc")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/sanity", methods=['GET'])
def init():
    return "",200

@app.route('/question', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        data = request.get_json()
        qname = data['question_text']
        qtype = data['question_type']
        qcat = data['question_category']
        qans = data['answer_choices']
        anstype = data['answer_type']
        return jsonify({'raspunsuri' : qans[0]})
    else:
        return 'Content-Type not supported!'