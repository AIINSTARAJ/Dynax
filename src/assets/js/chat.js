document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    // Sample responses for demo purposes (would be replaced with backend API calls)
    const botResponses = [
        "I've analyzed your request and found some interesting insights!",
        "Based on the data, here are my recommendations...",
        "I need more information to provide a complete analysis. Could you elaborate?",
        "Here's what I found in my database about your query...",
        "That's an interesting question! Let me process that...",
        "I've run several algorithms and here are the results of my analysis..."
    ];

    // Function to add a message to the chat
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message');
        messageDiv.classList.add(isUser ? 'user-message' : 'bot-message');
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'bot-message', 'typing-indicator-container');
        typingDiv.id = 'typing-indicator';
        
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('typing-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.classList.add('typing-dot');
            typingIndicator.appendChild(dot);
        }
        
        typingDiv.appendChild(typingIndicator);
        chatMessages.appendChild(typingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Function to simulate bot response (would be replaced with actual API call)
    function getBotResponse(message) {
        return new Promise((resolve) => {
            // Simulate API delay
            const responseTime = 1000 + Math.random() * 2000;
            
            setTimeout(() => {
                // In a real implementation, this would be an API call to your backend

               /*const response =  fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(
                        {'doi': doi,
                        'user': auth}
                    ),
                });
            
                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);    
                }*/

                const randomIndex = Math.floor(Math.random() * botResponses.length);
                resolve(botResponses[randomIndex]);

            }, responseTime);
        });
    }

    // Function to handle sending a message
    async function sendMessage() {
        const message = messageInput.value.trim();
        
        if (message === '') return;
        
        // Add user message to chat
        addMessage(message, true);
        messageInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Get bot response (would be API call in production)
            const response = await getBotResponse(message);
            
            // Remove typing indicator and add bot response
            removeTypingIndicator();
            
            // Add bot response with typewriter effect
            const botMessageDiv = document.createElement('div');
            botMessageDiv.classList.add('message', 'bot-message');
            chatMessages.appendChild(botMessageDiv);
            
            // Typewriter effect
            let i = 0;
            const typeWriter = () => {
                if (i < response.length) {
                    botMessageDiv.textContent += response.charAt(i);
                    i++;
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                    setTimeout(typeWriter, 20 + Math.random() * 10);
                }
            };
            
            typeWriter();
            
        } catch (error) {
            // Handle error
            removeTypingIndicator();
            addMessage("Sorry, I encountered an error processing your request.", false);
            console.error("Error getting bot response:", error);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Focus input on page load
    messageInput.focus();

    // Initialize with focus indicator
    messageInput.addEventListener('focus', () => {
        messageInput.style.borderColor = getComputedStyle(document.documentElement).getPropertyValue('--accent-color').trim();;
    });
    
    messageInput.addEventListener('blur', () => {
        messageInput.style.borderColor = 'rgba(255, 255, 255, 0.2)';
    });
});