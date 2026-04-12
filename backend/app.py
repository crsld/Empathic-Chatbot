from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle, random, re, nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('wordnet')

app = Flask(__name__)
CORS(app)

model        = pickle.load(open('../models/emotion_model.pkl', 'rb'))
vectorizer   = pickle.load(open('../models/vectorizer.pkl', 'rb'))
label_encoder = pickle.load(open('../models/label_encoder.pkl', 'rb'))

lemmatizer = WordNetLemmatizer()
distress_counter = {'count': 0}

def clean_text(text):
    text = text.lower()
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^\w\s.!?]', '', text)
    return text

def tokenize_lemmatize(text):
    tokens = word_tokenize(text)
    return " ".join([lemmatizer.lemmatize(w) for w in tokens])

def predict_emotion(text):
    text = tokenize_lemmatize(clean_text(text))
    vec  = vectorizer.transform([text])
    pred = model.predict(vec)
    return label_encoder.inverse_transform(pred)[0]

RESPONSES = {
    'sadness': {
        'casual':  ["I hear you. Want to tell me more?",
                    "That sounds really heavy. I'm here to listen."],
        'comfort': ["You don't have to go through this alone.",
                    "I care about how you're feeling right now."],
        'advice':  ["Try reaching out to someone you trust.",
                    "Journaling or a short walk can sometimes help process heavy feelings."],
    },
    'anger': {
        'casual':  ["Sounds like something really got to you. What happened?",
                    "I can feel the frustration. Want to talk about it?"],
        'comfort': ["Your feelings are completely valid. I'm here.",
                    "Let it out — this is a safe space."],
        'advice':  ["Try slow deep breaths before responding to the situation.",
                    "Stepping away briefly can help you feel calmer."],
    },
    'fear': {
        'casual':  ["That sounds really unsettling. Do you want to talk through it?",
                    "Fear can be overwhelming. I'm listening."],
        'comfort': ["You're not alone in this. I'm right here with you.",
                    "Whatever you're scared of, you don't have to face it alone."],
        'advice':  ["Try naming 5 things you can see around you — it helps ground you.",
                    "Talking to someone you trust about fears can really lighten the load."],
    },
    'joy': {
        'casual':  ["That's wonderful! Tell me more about what's making you happy!",
                    "I love hearing that! What's going on?"],
        'comfort': ["You deserve this happiness!",
                    "I'm really glad you're in a good place right now."],
        'advice':  ["Write down what's making you happy — it helps on harder days.",
                    "Sharing joy with others can multiply it!"],
    },
    'neutral': {
        'casual':  ["I'm here if you want to share anything more.",
                    "Okay! Anything on your mind you'd like to talk about?"],
        'comfort': ["I'm here for you, whatever you need.",
                    "You can always talk to me — no pressure at all."],
        'advice':  ["Checking in with yourself daily is a healthy habit.",
                    "Even on quiet days, it helps to be kind to yourself."],
    },
}
RESPONSES['surprise'] = RESPONSES['neutral']
RESPONSES['disgust']  = RESPONSES['neutral']

@app.route('/chat', methods=['POST'])
def chat():
    data       = request.json
    user_input = data.get('message', '')
    mode       = data.get('mode', 'casual')

    emotion = predict_emotion(user_input)

    if emotion in ['sadness', 'fear', 'anger']:
        distress_counter['count'] += 1
    else:
        distress_counter['count'] = 0

    suggestion = None
    if distress_counter['count'] >= 3 and mode == 'casual':
        mode = 'comfort'
        suggestion = "I've noticed you've been going through a lot. I've switched to comfort mode — you can also try the Advice button if you'd like."

    pool     = RESPONSES.get(emotion, RESPONSES['neutral'])
    response = random.choice(pool.get(mode, pool['casual']))

    return jsonify({
        'response':  response,
        'emotion':   emotion,
        'suggestion': suggestion
    })

if __name__ == '__main__':
    app.run(debug=True)