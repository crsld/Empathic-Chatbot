# fix_lstm.py  — run once from backend/ folder
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Embedding, Conv1D, Dropout, Bidirectional, LSTM, Dense
)
from tensorflow.keras.optimizers import Adam

print("Step 1: Rebuilding model architecture...")
model = Sequential([
    Embedding(input_dim=15000, output_dim=128),
    Conv1D(filters=128, kernel_size=5, padding='same', activation='relu'),
    Dropout(0.3),
    Bidirectional(LSTM(128, return_sequences=True)),
    Dropout(0.4),
    Bidirectional(LSTM(64, return_sequences=False)),
    Dropout(0.3),
    Dense(128, activation='relu'),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(7, activation='softmax'),
])

model.compile(
    optimizer=Adam(learning_rate=0.0007, clipnorm=1.0),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# ── Build the model first with dummy data (fixes the error)
print("Step 2: Building model with dummy data...")
dummy_input = np.zeros((1, 150), dtype='int32')
model(dummy_input)
print("✅ Model built.")

print("Step 3: Loading weights from old model...")
model.load_weights('../models/lstm_model.keras')
print("✅ Weights loaded.")

print("Step 4: Saving fixed model...")
model.save('../models/lstm_model_fixed.keras')
print("✅ Saved as lstm_model_fixed.keras")
print("\n✅ Done! Now rename lstm_model_fixed.keras → lstm_model.keras in your models/ folder.")