const messagesEl = document.getElementById('chatMessages');
const inputEl    = document.getElementById('userInput');
const sendBtn    = document.getElementById('sendBtn');
const modeBtns   = document.querySelectorAll('.mode-btn');

let currentMode = 'casual';

// Dynamic Textarea
inputEl.addEventListener('input', () => {
  sendBtn.disabled = inputEl.value.trim() === '';
  inputEl.style.height = 'auto';
  inputEl.style.height = inputEl.scrollHeight + 'px';
});

// Mode Selector logic
modeBtns.forEach(btn => {
  btn.addEventListener('click', () => {
    modeBtns.forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    currentMode = btn.dataset.mode;
  });
});

function addMessage(text, sender, isBot = false) {
  const div = document.createElement('div');
  div.className = `message ${sender} fade-in`;
  div.innerHTML = `<div class="bubble">${text}</div>`;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

function showTypingIndicator() {
  const div = document.createElement('div');
  div.className = 'message bot fade-in';
  div.innerHTML = `
    <div class="bubble typing-dots">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>`;
  messagesEl.appendChild(div);
  messagesEl.scrollTop = messagesEl.scrollHeight;
  return div;
}

async function sendMessage() {
  const text = inputEl.value.trim();
  if (!text) return;

  addMessage(text, 'user');
  inputEl.value = '';
  inputEl.style.height = 'auto';
  sendBtn.disabled = true;

  const typingEl = showTypingIndicator();

  try {
    const res = await fetch('http://127.0.0.1:5000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, mode: currentMode })
    });

    const data = await res.json();
    typingEl.remove();

    const botDiv = document.createElement('div');
    botDiv.className = 'message bot fade-in';
    botDiv.innerHTML = `
        <div class="bubble">${data.response}</div>
        <div class="emotion-tag">Feeling: ${data.emotion}</div>
        ${data.suggestion ? `<div class="suggestion-box">${data.suggestion}</div>` : ''}
    `;
    messagesEl.appendChild(botDiv);
    messagesEl.scrollTop = messagesEl.scrollHeight;

  } catch (err) {
    typingEl.remove();
    addMessage('Connection lost. Please check the server.', 'bot');
  }
}

// Enter Key Logic
inputEl.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    if (!sendBtn.disabled) sendMessage();
  }
});

sendBtn.addEventListener('click', sendMessage);