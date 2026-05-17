# test_models.py
# Run this from inside the backend/ folder:  python test_models.py

import pickle, sys

PASS = "✅"
FAIL = "❌"

def section(title):
    print(f"\n{'─'*40}")
    print(f"  {title}")
    print(f"{'─'*40}")

# ── LR Model
section("Logistic Regression Models")
try:
    lr_model      = pickle.load(open('../models/lr_model.pkl',      'rb'))
    vectorizer    = pickle.load(open('../models/vectorizer.pkl',     'rb'))
    label_encoder = pickle.load(open('../models/label_encoder.pkl', 'rb'))

    # Quick prediction test
    test_vec  = vectorizer.transform(["I feel really sad today"])
    test_pred = lr_model.predict(test_vec)
    result    = label_encoder.inverse_transform(test_pred)[0]
    print(f"{PASS} lr_model.pkl       loaded")
    print(f"{PASS} vectorizer.pkl     loaded")
    print(f"{PASS} label_encoder.pkl  loaded")
    print(f"{PASS} Test prediction:   '{result}'")
except Exception as e:
    print(f"{FAIL} LR model error: {e}")
    sys.exit(1)   # LR is required — stop if it fails

# ── LSTM Model
section("LSTM Model")
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    lstm_model     = load_model('../models/lstm_model.keras')
    tokenizer_lstm = pickle.load(open('../models/tokenizer_lstm.pkl', 'rb'))

    # Quick prediction test
    seq  = tokenizer_lstm.texts_to_sequences(["I feel really sad today"])
    pad  = pad_sequences(seq, maxlen=150, padding='post', truncating='post')
    pred = lstm_model.predict(pad, verbose=0)
    result = label_encoder.inverse_transform([pred.argmax()])[0]
    print(f"{PASS} lstm_model.keras   loaded")
    print(f"{PASS} tokenizer_lstm.pkl loaded")
    print(f"{PASS} Test prediction:   '{result}'")
except Exception as e:
    print(f"⚠️  LSTM skipped (optional): {e}")

# ── BERT Model
section("BERT Model")
try:
    from transformers import BertTokenizer, BertForSequenceClassification
    import torch
    bert_model     = BertForSequenceClassification.from_pretrained('../models/bert_emotion_model')
    bert_tokenizer = BertTokenizer.from_pretrained('../models/bert_emotion_model')
    bert_model.eval()

    # Quick prediction test
    inputs = bert_tokenizer("I feel really sad today",
                            return_tensors='pt', truncation=True,
                            padding=True, max_length=128)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    pred   = outputs.logits.argmax(dim=1).item()
    result = label_encoder.inverse_transform([pred])[0]
    print(f"{PASS} bert_emotion_model loaded")
    print(f"{PASS} Test prediction:   '{result}'")
except Exception as e:
    print(f"⚠️  BERT skipped (optional): {e}")

# ── Done
print(f"\n{'═'*40}")
print("  🎉 All required models loaded successfully!")
print(f"{'═'*40}\n")# test_models.py
# Run this from inside the backend/ folder:  python test_models.py

import pickle, sys

PASS = "✅"
FAIL = "❌"

def section(title):
    print(f"\n{'─'*40}")
    print(f"  {title}")
    print(f"{'─'*40}")

# ── LR Model
section("Logistic Regression Models")
try:
    lr_model      = pickle.load(open('../models/lr_model.pkl',      'rb'))
    vectorizer    = pickle.load(open('../models/vectorizer.pkl',     'rb'))
    label_encoder = pickle.load(open('../models/label_encoder.pkl', 'rb'))

    # Quick prediction test
    test_vec  = vectorizer.transform(["I feel really sad today"])
    test_pred = lr_model.predict(test_vec)
    result    = label_encoder.inverse_transform(test_pred)[0]
    print(f"{PASS} lr_model.pkl       loaded")
    print(f"{PASS} vectorizer.pkl     loaded")
    print(f"{PASS} label_encoder.pkl  loaded")
    print(f"{PASS} Test prediction:   '{result}'")
except Exception as e:
    print(f"{FAIL} LR model error: {e}")
    sys.exit(1)   # LR is required — stop if it fails

# ── LSTM Model
section("LSTM Model")
try:
    from tensorflow.keras.models import load_model
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    lstm_model     = load_model('../models/lstm_model.keras')
    tokenizer_lstm = pickle.load(open('../models/tokenizer_lstm.pkl', 'rb'))

    # Quick prediction test
    seq  = tokenizer_lstm.texts_to_sequences(["I feel really sad today"])
    pad  = pad_sequences(seq, maxlen=150, padding='post', truncating='post')
    pred = lstm_model.predict(pad, verbose=0)
    result = label_encoder.inverse_transform([pred.argmax()])[0]
    print(f"{PASS} lstm_model.keras   loaded")
    print(f"{PASS} tokenizer_lstm.pkl loaded")
    print(f"{PASS} Test prediction:   '{result}'")
except Exception as e:
    print(f"⚠️  LSTM skipped (optional): {e}")

# ── BERT Model
section("BERT Model")
try:
    from transformers import BertTokenizer, BertForSequenceClassification
    import torch
    bert_model     = BertForSequenceClassification.from_pretrained('../models/bert_emotion_model')
    bert_tokenizer = BertTokenizer.from_pretrained('../models/bert_emotion_model')
    bert_model.eval()

    # Quick prediction test
    inputs = bert_tokenizer("I feel really sad today",
                            return_tensors='pt', truncation=True,
                            padding=True, max_length=128)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    pred   = outputs.logits.argmax(dim=1).item()
    result = label_encoder.inverse_transform([pred])[0]
    print(f"{PASS} bert_emotion_model loaded")
    print(f"{PASS} Test prediction:   '{result}'")
except Exception as e:
    print(f"⚠️  BERT skipped (optional): {e}")

# ── Done
print(f"\n{'═'*40}")
print("  🎉 All required models loaded successfully!")
print(f"{'═'*40}\n")