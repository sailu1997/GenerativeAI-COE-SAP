let chatMessages = [];

document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-msg');
    const sendButton = document.getElementById('send-button');

    loadChatMessages();

    sendButton.addEventListener('click', function() {
        const userMessage = userInput.value;
        if (userMessage !== ''){
            displayMessage('user-msg', userMessage);
            simulateAITyping();
        }
        userInput.value = '';
    });

    function simulateAITyping() {
        setTimeout(function() {
            displayMessage('ai-msg', 'Let me think...');   
        }, 1000);
    }

    function displayMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.classList.add(sender);
        messageElement.innerHTML = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;

        chatMessages.push({
            sender: sender,
            message: message
        });
    }

    function loadChatMessages() {
        chatMessages.forEach(function(chatMessage) {
            displayMessage(chatMessage.sender, chatMessage.message);
        });
    }
});
