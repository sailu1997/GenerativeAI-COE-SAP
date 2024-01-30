let chatMessages = [];

document.addEventListener('DOMContentLoaded', function() {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-msg');
    const sendButton = document.getElementById('send-button');

    loadChatMessages();

    document.querySelectorAll('.feedback-button').forEach(button => {
        button.addEventListener('click', function() {
            const feedbackType = this.classList.contains('thumbs-up') ? 'positive' : 'negative';
            console.log(feedbackType);
            sendFeedback(feedbackType);
        });
    });

    function sendFeedback(feedbackValue) {
        fetch('/submit-feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ feedback: feedbackValue })
        })
        .then(response => response.json())
        .then(data => console.log('Success:', data))
        .catch(error => console.error('Error:', error));
    }

    sendButton.addEventListener('click', function() {
        const userMessage = userInput.value;
        if (userMessage !== '') {
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
