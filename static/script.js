const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatArea = document.getElementById('chat-area');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    // Add user message to UI
    appendMessage(message, 'user');
    userInput.value = '';

    // Show typing indicator
    const typingId = showTypingIndicator();

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);

        // Add bot response to UI
        appendMessage(data.response, 'bot');
    } catch (error) {
        removeTypingIndicator(typingId);
        appendMessage("Sorry, something went wrong. Please check your connection.", 'bot');
        console.error('Error:', error);
    }
});

function appendMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', `${sender}-message`);

    const avatarDiv = document.createElement('div');
    avatarDiv.classList.add('avatar');
    avatarDiv.textContent = sender === 'user' ? 'You' : 'AI';

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('content');
    contentDiv.textContent = text;

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatArea.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function showTypingIndicator() {
    const id = 'typing-' + Date.now();
    
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'bot-message');
    messageDiv.id = id;

    const avatarDiv = document.createElement('div');
    avatarDiv.classList.add('avatar');
    avatarDiv.textContent = 'AI';

    const contentDiv = document.createElement('div');
    contentDiv.classList.add('content');
    contentDiv.innerHTML = `
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;

    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);
    
    chatArea.appendChild(messageDiv);
    chatArea.scrollTop = chatArea.scrollHeight;
    
    return id;
}

function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}
