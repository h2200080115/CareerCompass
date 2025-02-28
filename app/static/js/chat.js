const chatMessages = document.getElementById('chat-messages');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message) return;
    
    // Add user message
    addMessage(message, 'user');
    userInput.value = '';
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            addMessage(data.response, 'assistant');
        } else {
            addMessage('Sorry, I encountered an error. Please try again.', 'system');
        }
    } catch (error) {
        console.error('Chat error:', error);
        addMessage('Sorry, I encountered an error. Please try again.', 'system');
    }
});

function addMessage(message, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `${type}-message mb-3`;
    messageDiv.textContent = message;
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}
