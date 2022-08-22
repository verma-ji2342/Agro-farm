from chatterbot import ChatBot
from chatterbot.conversation import Statement
from chatterbot.trainers import ListTrainer
from flask import Flask, render_template, request, make_response
from flask_cors import CORS, cross_origin

import json

app = Flask(__name__, static_url_path='/templates', static_folder='/templates', template_folder='/templates')
cors = CORS(app, resources={r"/jarvis": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


DEFAULT_ANSWER = "I'm just 3 days old right now and I haven't grasped your language that well but I'm trying! 😉"

bot = ChatBot(
    "jarvis",
    logic_adapters=[
        'chatterbot.logic.MathematicalEvaluation',
        'chatterbot.logic.BestMatch',
    ],
    database_uri='sqlite:///db.sqlite3'
)

#
trainer = ListTrainer(bot)
#
# dataCollection = []
# with open('C:\\Users\\Lenovo\\Downloads\\archive\\Ubuntu-dialogue-corpus\\dialogueText.csv', encoding='utf-8') as trainingData:
#     for line in trainingData:
#         dataSet = line.split(",")
#         dataCollection.append(dataSet[5])
#
# print("length", len(dataCollection))
# trainer.train(dataCollection)


def process_data(data):
    result = bot.generate_response(Statement(data))
    if len(result.text) == 1:
        return DEFAULT_ANSWER
    return result.text


def train_data(data_q, data_a):
    trainer.train([data_q, data_a])


@app.route('/')
@cross_origin()
def hello_world():
    return render_template('index.html')


@app.route('/jarvis', methods=["GET", "POST"])
@cross_origin()
def jarvis():
    if request.method == 'GET':
        print(request)
        return make_response({"response": "Hello, this is an invalid request!"})
    elif request.method == 'POST':
        try:
            return make_response({"response": process_data(request.data.decode('utf-8')[9:-2])})
        except Exception as e:
            return make_response({"error": repr(e)})


@app.route('/help_jarvis', methods=["GET", "POST"])
@cross_origin()
def evolve_jarvis():
    if request.method == "GET":
        return make_response({"response": "Hello, this is an invalid request!"})
    elif request.method == "POST":
        try:
            json_data = request.data.decode('utf-8')
            data_dict = json.loads(json_data)
            train_data(data_dict.get("data_q", ""), data_dict.get("data_a", ""))
            print(data_dict)
            return make_response({"response": "success"})
        except Exception as e:
            return make_response({"error": repr(e)})


if __name__ == '__main__':
    app.run()
