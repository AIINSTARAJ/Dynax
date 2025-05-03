// chat.js - Enhanced client-side chat functionality for Dynax research assistant

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const clearChatButton = document.getElementById('clear-chat');
    const exportChatButton = document.getElementById('export-chat');
    const attachButton = document.getElementById('attach-button');
    const newChatButton = document.getElementById('new-chat');
    const conversationList = document.getElementById('conversation-list');
    
    // State
    const state = {
      messages: [],
      currentConversationId: generateId(),
      isTyping: false
    };
    
    // Initialize UI behaviors
    initTextareaAutoResize();
    initButtonStates();
    initScrollHandling();
    initAnimations();
    
    // Event listeners
    messageInput.addEventListener('input', handleInput);
    sendButton.addEventListener('click', handleSendMessage);
    messageInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        handleSendMessage();
      }
    });
    
    clearChatButton.addEventListener('click', handleClearChat);
    exportChatButton.addEventListener('click', handleExportChat);
    attachButton.addEventListener('click', handleAttachment);
    newChatButton.addEventListener('click', handleNewChat);
    
    // Handle menu toggle for mobile
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (menuToggle) {
      menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
        menuToggle.classList.toggle('active');
      });
    }
    
    // Functions
    function initTextareaAutoResize() {
      messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
      });
    }
    
    function initButtonStates() {
      messageInput.addEventListener('input', () => {
        sendButton.disabled = messageInput.value.trim() === '';
      });
    }
    
    function initScrollHandling() {
      // Auto-scroll to bottom on new messages
      const observer = new MutationObserver(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
      });
      
      observer.observe(chatMessages, { childList: true });
    }
    
    function initAnimations() {
      // GSAP animations for various elements
      gsap.from('.chat-container', {
        opacity: 0,
        y: 20,
        duration: 0.6,
        ease: 'power2.out'
      });
      
      // Animate floating shapes
      gsap.to('.shape-1', {
        x: 20,
        y: -20,
        rotation: 20,
        duration: 25,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut'
      });
      
      gsap.to('.shape-2', {
        x: -15,
        y: 15,
        rotation: -15,
        duration: 20,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        delay: 0.5
      });
      
      gsap.to('.shape-3', {
        x: 25,
        y: 10,
        rotation: 10,
        duration: 22,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        delay: 1
      });
      
      gsap.to('.shape-4', {
        x: -10,
        y: -15,
        rotation: -5,
        duration: 18,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        delay: 1.5
      });
    }
    
    function handleInput() {
      // Enable/disable send button based on input
      sendButton.disabled = messageInput.value.trim() === '';
      
      // Auto-resize textarea
      messageInput.style.height = 'auto';
      messageInput.style.height = (messageInput.scrollHeight) + 'px';
    }
    
    async function handleSendMessage() {
      const message = messageInput.value.trim();
      if (!message || state.isTyping) return;
      
      // Reset input
      messageInput.value = '';
      messageInput.style.height = 'auto';
      sendButton.disabled = true;
      
      // Add user message to UI
      addMessageToUI('user', message);
      
      // Show typing indicator
      showTypingIndicator();
      
      try {
        // Send message to backend
        const response = await sendMessageToBackend(message);
        
        // Remove typing indicator and display response
        removeTypingIndicator();
        
        // Process and display the bot's response
        if (response && response.response) {
          addMessageToUI('bot', response.response, true);
        } else {
          addMessageToUI('bot', 'Sorry, I encountered an error processing your request.');
        }
      } catch (error) {
        console.error('Error sending message:', error);
        removeTypingIndicator();
        addMessageToUI('bot', 'Sorry, there was an error communicating with the server.');
      }
    }
    
    async function sendMessageToBackend(message) {
      state.isTyping = true;
      
      try {
        const response = await fetch('/bot', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ msg: message })
        });
        
        const data = await response.json();
        return data;
      } finally {
        state.isTyping = false;
      }
    }
    
    function addMessageToUI(sender, content, isHTML = false) {
      const messageElement = document.createElement('div');
      messageElement.className = `message ${sender}-message`;
      
      const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
      
      // Create avatar with first letter
      const avatarContent = sender === 'user' ? 'U' : 'D!';
      
      messageElement.innerHTML = `
        <div class="message-avatar">${avatarContent}</div>
        <div class="message-content">
          <div class="message-bubble">
            ${isHTML ? content : `<p>${content}</p>`}
          </div>
          <div class="message-time">${time}</div>
        </div>
      `;
      
      // Add message to UI
      chatMessages.appendChild(messageElement);
      
      // Scroll to bottom
      chatMessages.scrollTop = chatMessages.scrollHeight;
      
      // Add message to state
      state.messages.push({
        sender,
        content,
        timestamp: new Date().toISOString()
      });
      
      // Apply typing animation for bot messages
      if (sender === 'bot' && !isHTML) {
        applyTypingAnimation(messageElement.querySelector('p'));
      }
    }
    
    function showTypingIndicator() {
      const indicator = document.createElement('div');
      indicator.className = 'message bot-message typing-message';
      indicator.innerHTML = `
        <div class="message-avatar">D!</div>
        <div class="typing-indicator">
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        </div>
      `;
      chatMessages.appendChild(indicator);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    function removeTypingIndicator() {
      const typingMessage = document.querySelector('.typing-message');
      if (typingMessage) {
        typingMessage.remove();
      }
    }
    
    function applyTypingAnimation(element) {
      const text = element.textContent;
      element.textContent = '';
      
      // Split by words for a more natural animation
      const words = text.split(' ');
      let i = 0;
      
      // Function to add one word at a time
      function addNextWord() {
        if (i < words.length) {
          element.textContent += (i > 0 ? ' ' : '') + words[i];
          i++;
          setTimeout(addNextWord, Math.max(10, Math.min(50, words[i-1].length * 20)));
        }
      }
      
      // Start the typing animation
      addNextWord();
    }
    
    function handleClearChat() {
      if (confirm('Are you sure you want to clear this conversation?')) {
        // Clear the UI
        while (chatMessages.children.length > 1) {
          chatMessages.removeChild(chatMessages.lastChild);
        }
        
        // Reset state
        state.messages = [];
        
        // Add initial message
        addMessageToUI('bot', 'Conversation cleared. How can I help with your research?');
      }
    }
    
    function handleExportChat() {
      // Create chat transcript
      let transcript = "# Dynax Research Conversation\n\n";
      transcript += `Date: ${new Date().toLocaleDateString()}\n\n`;
      
      state.messages.forEach(msg => {
        const sender = msg.sender === 'user' ? 'You' : 'Dynax';
        transcript += `**${sender}**: ${stripHtml(msg.content)}\n\n`;
      });
      
      // Create and download file
      const blob = new Blob([transcript], { type: 'text/markdown' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `dynax-research-${new Date().toISOString().split('T')[0]}.md`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }
    
    function stripHtml(html) {
      const temp = document.createElement('div');
      temp.innerHTML = html;
      return temp.textContent || temp.innerText || '';
    }
    
    function handleAttachment() {
      // Placeholder for file attachment functionality
      alert('File attachment functionality coming soon!');
    }
    
    function handleNewChat() {
      // Create new conversation
      const newConvoId = generateId();
      state.currentConversationId = newConvoId;
      
      // Add to sidebar
      addConversationToSidebar('New Research', newConvoId, true);
      
      // Clear messages
      while (chatMessages.children.length > 0) {
        chatMessages.removeChild(chatMessages.lastChild);
      }
      
      // Reset state
      state.messages = [];
      
      // Add initial message
      addMessageToUI('bot', 'Hello! I\'m Dynax, your academic research assistant. How can I help with your research today?');
    }
    
    function addConversationToSidebar(title, id, isActive = false) {
      // Clear active state from all conversations
      document.querySelectorAll('.conversation-item').forEach(item => {
        item.classList.remove('active');
      });
      
      // Create new conversation item
      const convoItem = document.createElement('div');
      convoItem.className = `conversation-item ${isActive ? 'active' : ''}`;
      convoItem.dataset.id = id;
      convoItem.innerHTML = `
        <i class="fas fa-comments"></i>
        <span>${title}</span>
      `;
      
      // Add click handler
      convoItem.addEventListener('click', () => {
        // Handle conversation switching (placeholder)
        document.querySelectorAll('.conversation-item').forEach(item => {
          item.classList.remove('active');
        });
        convoItem.classList.add('active');
      });
      
      // Add to sidebar
      conversationList.appendChild(convoItem);
    }
    
    function generateId() {
      return Math.random().toString(36).substring(2, 15);
    }
    
    // Initialize with welcome message
    // First message is already in HTML
  });