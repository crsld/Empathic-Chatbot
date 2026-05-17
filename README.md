# Empathic Chatbot 🤖💬

A mental health chatbot that detects emotions from user input and responds empathetically.

## Features
- Emotion detection using Logistic Regression and LSTM models
- Three response modes: Casual, Comfort, and Advice
- Auto-switches to Comfort mode after detecting repeated distress
- REST API built with Flask

## Project Structure

## Setup Instructions

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Flask server
```bash
python app.py
```

### 3. Open the frontend
Open `frontend/index.html` in your browser.

## Models Used
| Model | Status |
|-------|--------|
| Logistic Regression | ✅ Active |
| LSTM (Bidirectional) | ✅ Active |
| BERT | ⚠️ Optional |

## Tech Stack
- Python, Flask, scikit-learn, TensorFlow/Keras
- HTML, CSS, JavaScript
