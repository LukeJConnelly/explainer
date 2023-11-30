from flask import Flask, request, jsonify
from flask_cors import CORS
import string
import re

app = Flask(__name__)
CORS(app)

sentences = [
    "jeg elsker at spille fodbold og drømmer om at blive en professionel fodboldspiller en dag",
    "musik er min store passion og jeg spiller guitar i mit eget band",
    "jeg elsker at læse fantasybøger og drømmer om at skrive min egen en dag",
    "matematik er min yndlingsfag og jeg elsker at løse komplekse problemer",
    "naturen er mit fristed og jeg elsker at vandre og udforske skove og bjerge",
    "jeg er en dyreelsker og har en samling af kæledyr derhjemme",
    "at tegne og male er min kreative udfoldelse og jeg drømmer om at blive en kunstner",
    "jeg bruger meget tid på at spille videospil og konkurrere online med mine venner",
    "jeg interesserer mig for historie og drømmer om at arbejde som arkæolog en dag",
    "jeg elsker at lave mad og eksperimentere med forskellige opskrifter",
    "jeg er en ivrig science fiction-fan og elsker at se rumfart og science fiction-film",
    "jeg bruger meget tid på at hjælpe i lokalsamfundet og frivilligt arbejde",
    "jeg er en teaterentusiast og elsker at optræde på scenen",
    "jeg elsker at rejse og udforske nye kulturer og steder",
    "jeg er en dygtig programmerer og elsker at skabe computerprogrammer",
    "jeg er en konkurrencemenneske og elsker at deltage i sportsbegivenheder",
    "jeg er en dedikeret studerende og stræber altid efter at opnå gode karakterer",
    "jeg drømmer om at blive astronaut og udforske rummet",
    "jeg elsker at skrive digte og noveller som en form for selvudtryk",
    "jeg er en positiv person og forsøger altid at sprede glæde omkring mig",
]

state = 'clean'

@app.route('/add', methods=['POST'])
def submit_sentence():
    data = request.get_json()
    sentence = data.get('sentence')
    sentences.append(sentence)
    return jsonify({'message': 'Sentence submitted successfully.'})

@app.route('/remove', methods=['POST'])
def remove_sentence():
    data = request.get_json()
    sentence = data.get('sentence')
    del sentences[sentence]
    return jsonify({'message': 'Sentence deleted successfully.'})

@app.route('/state', methods=['POST'])
def submit_state():
    data = request.get_json()
    global state
    state = data.get('state')
    return jsonify({'message': 'State submitted successfully.'})


def cleaned(s):
    return re.sub(r'\s+', ' ', s.translate(str.maketrans('', '', string.punctuation))).lower().strip()

@app.route('/')
def get_state():
    return jsonify({'sentences': [cleaned(s) for s in sentences], 'state': state})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)