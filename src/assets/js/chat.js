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


    // Function to simulate bot response (with actual API call)
    async function getBotResponse(message) {
        const res = await fetch('/bot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ msg: message }),
        });
    
        if (!res.ok) {
            throw new Error(`HTTP error! Status: ${res.status}`);
        }
    
        const data = await res.json();
        return data.response; 
    }
    

   /* async function sendMessage() {
        const message = messageInput.value.trim();
        
        if (message === '') return;
        
        // Add user message to chat
        addMessage(message, true);

        messageInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        try {
            // Get bot response (would be API call in production)
            const content = await getBotResponse(message);
            const cleanRes = DOMPurify.sanitize(content);
            
            // Remove typing indicator and add bot response
            removeTypingIndicator();
            
            // Add bot response with typewriter effect
            const botMessageDiv = document.createElement('div');
            botMessageDiv.classList.add('message', 'bot-message');
            chatMessages.appendChild(botMessageDiv);
            
            // Typewriter effect
            let i = 0;
            const typeWriter = () => {
                if (i < content.length) {
                    botMessageDiv.textContent += cleanRes.charAt(i);
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
    }*/

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
                const content = await getBotResponse(message);
                
                // Sanitize the content to ensure no harmful code
                const cleanRes = DOMPurify.sanitize(content);
                
                // Decode HTML entities to allow rendering of tags
                const decodedContent = decodeHtmlEntities(cleanRes);
                
                // Remove typing indicator and add bot response
                removeTypingIndicator();
                
                // Add bot message div to the chat
                const botMessageDiv = document.createElement('div');
                botMessageDiv.classList.add('message', 'bot-message');
                chatMessages.appendChild(botMessageDiv);
                
                // Typewriter effect
                let i = 0;
                let typedContent = ''; // Accumulate the typed content
        
                const typeWriter = () => {
                    if (i < decodedContent.length) {
                        typedContent += decodedContent.charAt(i); // Add the next character to the content
                        botMessageDiv.textContent = typedContent;  // Update text content (no HTML yet)
                        i++;
                        chatMessages.scrollTop = chatMessages.scrollHeight;
                        setTimeout(typeWriter, 20 + Math.random() * 10);
                    } else {
                        // Once typing is complete, set the innerHTML to decoded content
                        botMessageDiv.innerHTML = typedContent; // Now inject HTML
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
        
        // Decode HTML entities back to proper HTML
        function decodeHtmlEntities(text) {
            const textArea = document.createElement('textarea');
            textArea.innerHTML = text;
            return textArea.value;
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