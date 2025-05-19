document.addEventListener("DOMContentLoaded", function () {
    // Elements
    const analyzeButton = document.getElementById("btn-ls");
    const analysisContent = document.querySelector(".analysis-content");
    const analysisHeader = document.querySelector(".analysis-header");
    const loadingContainer = document.querySelector(".loading-container");
    const doiElement = document.getElementById("res-doi");
    const titleElement = document.getElementById("title");
    const mobileMenuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.nav-links');
    const hamburger = document.querySelector('.hamburger');
    
    // Extract DOI from the element text
    const doiText = doiElement ? doiElement.innerText.trim() : "";
    const doi = doiText.replace(/DOI - /i, "").trim();
    
    // Get paper title
    const title = titleElement ? titleElement.innerText.trim() : "";
    
    // Get auth token if available
    const authTokenElement = document.getElementById("auth-token");
    const authToken = authTokenElement ? authTokenElement.innerText.trim() : "";
    
    // Mobile menu toggle
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        const isClickInsideNav = navLinks.contains(event.target);
        const isClickOnToggle = mobileMenuToggle.contains(event.target);
        
        if (!isClickInsideNav && !isClickOnToggle && navLinks.classList.contains('active')) {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
        }
    });
    
    // GSAP animations for page elements
    function initAnimations() {
        // Create timeline for sequence animations
        const tl = gsap.timeline();
        
        // Logo animation
        tl.from(".paper-logo", { 
            duration: 1, 
            y: -30, 
            opacity: 0, 
            ease: "power3.out" 
        });
        
        // Title animation
        tl.from(".paper-title", { 
            duration: 1, 
            y: 20, 
            opacity: 0, 
            ease: "power3.out" 
        }, "-=0.5");
        
        // Authors animation
        tl.from(".paper-authors", { 
            duration: 1, 
            y: 20, 
            opacity: 0, 
            ease: "power3.out" 
        }, "-=0.7");
        
        // Badges animation with stagger
        tl.from(".paper-badges .paper-badge", { 
            duration: 0.8, 
            scale: 0.5, 
            opacity: 0, 
            stagger: 0.1, 
            ease: "back.out(1.7)" 
        }, "-=0.5");
        
        // Metadata card animation
        tl.from(".metadata-card", { 
            duration: 1, 
            y: 30, 
            opacity: 0, 
            ease: "power3.out" 
        }, "-=0.3");
        
        // Metadata items animation with stagger
        tl.from(".metadata-item", { 
            duration: 0.8, 
            x: -20, 
            opacity: 0, 
            stagger: 0.2, 
            ease: "power3.out" 
        }, "-=0.7");
        
        // Abstract section animation
        tl.from(".paper-abstract", { 
            duration: 1, 
            y: 40, 
            opacity: 0, 
            ease: "power3.out" 
        }, "-=0.4");
        
        // Action buttons animation with stagger
        tl.from(".action-button", { 
            duration: 0.8, 
            scale: 0.8, 
            opacity: 0, 
            stagger: 0.2, 
            ease: "back.out(1.5)" 
        }, "-=0.6");
        
        // Floating shapes animation for background elements
        gsap.to(".floating-shapes .shape", {
            y: "random(-20, 20)",
            x: "random(-20, 20)",
            rotation: "random(-15, 15)",
            duration: "random(3, 6)",
            ease: "sine.inOut",
            repeat: -1,
            yoyo: true,
            stagger: 0.5
        });
    }
    
    // Run animations
    initAnimations();
    
    // Show loading animation
    function showLoading() {
        // Reset any previous analysis
        analysisContent.innerHTML = "";
        analysisHeader.innerHTML = "";
        
        // Show loading container with animation
        loadingContainer.style.display = "flex";
        gsap.from(loadingContainer, {
            duration: 0.5,
            opacity: 0,
            y: 20
        });
        
        // Hide analysis sections
        analysisContent.classList.remove("visible");
        analysisHeader.classList.remove("visible");
        
        // Animate loading spinner
        gsap.to(".spinner-ring", {
            duration: 2,
            rotation: "+=360",
            repeat: -1,
            ease: "linear"
        });
        
        // Pulse animation for loading text
        gsap.to(".loading-text", {
            duration: 1.5,
            opacity: 0.6,
            yoyo: true,
            repeat: -1,
            ease: "sine.inOut"
        });
    }
    
    // Hide loading animation
    function hideLoading() {
        // Fade out loading container
        gsap.to(loadingContainer, {
            duration: 0.5,
            opacity: 0,
            onComplete: () => {
                // Hide container after fade
                loadingContainer.style.display = "none";
                loadingContainer.style.opacity = 1;
                
                // Reset loading text animation
                gsap.killTweensOf(".loading-text");
                
                // Show analysis header with animation
                setTimeout(() => {
                    analysisHeader.classList.add("visible");
                    
                    // Add a highlight flash effect to header
                    gsap.fromTo(analysisHeader, 
                        { textShadow: "0 0 10px rgba(0, 255, 255, 0.8)" },
                        { 
                            textShadow: "0 0 0px rgba(0, 255, 255, 0)",
                            duration: 1.5,
                            ease: "power2.out"
                        }
                    );
                    
                    // Show analysis content with delay
                    setTimeout(() => {
                        analysisContent.classList.add("visible");
                        
                        // Animate internal elements of analysis content
                        gsap.from(".analysis-content > *", {
                            y: 20,
                            opacity: 0,
                            stagger: 0.1,
                            duration: 0.6,
                            delay: 0.2,
                            ease: "power2.out"
                        });
                    }, 300);
                }, 200);
            }
        });
    }
    
    // Get AI analysis of the paper
    async function getAnalysis(doi) {
        // Show loading animation
        showLoading();
        
        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    'doi': doi,
                    'user': authToken
                }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const analysisHtml = await response.text();
            
            // Set content and titles
            analysisContent.innerHTML = analysisHtml;
            analysisHeader.innerHTML = `<i class="fas fa-robot"></i> Dynax! AI Analysis`;
            
            // Add social share buttons if needed
            addSocialShareButtons();
            
            // Highlight code blocks if they exist in the analysis
            if (window.hljs) {
                document.querySelectorAll('pre code').forEach((block) => {
                    hljs.highlightElement(block);
                });
            }
            
        } catch (error) {
            console.error('Error analyzing paper:', error);
            
            // Show error message in the analysis area
            analysisHeader.innerHTML = `<i class="fas fa-exclamation-triangle"></i> Analysis Error`;
            analysisContent.innerHTML = `
                <div class="error-message">
                    <p style='font-size:15px; color:var(--text-secondary);'>We encountered an error while analyzing this paper. Please try again later.</p>
                    <button class="retry-button" onclick="location.reload()">
                        <i class="fas fa-redo"></i> Retry
                    </button>
                </div>
            `;
            
        } finally {
            // Hide loading with a slight delay for better UX
            setTimeout(() => {
                hideLoading();
            }, 800);
        }
    }
    
    // Add social share buttons to analysis results
    function addSocialShareButtons() {
        const shareContainer = document.createElement('div');
        shareContainer.className = 'share-container';
        shareContainer.innerHTML = `
            <h3>Share this analysis:</h3>
            <div class="share-buttons">
                <button class="share-btn twitter">
                    <i class="fab fa-twitter"></i> Twitter
                </button>
                <button class="share-btn linkedin">
                    <i class="fab fa-linkedin"></i> LinkedIn
                </button>
                <button class="share-btn copy">
                    <i class="fas fa-link"></i> Copy Link
                </button>
            </div>
        `;
        
        // Append to analysis content
        analysisContent.appendChild(shareContainer);
        
        // Add event listeners to share buttons
        const twitterBtn = shareContainer.querySelector('.twitter');
        const linkedinBtn = shareContainer.querySelector('.linkedin');
        const copyBtn = shareContainer.querySelector('.copy');
        
        if (twitterBtn) {
            twitterBtn.addEventListener('click', () => {
                const shareText = `Check out this AI analysis of "${title}" on Dynax! Research`;
                const shareUrl = window.location.href;
                window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(shareUrl)}`, '_blank');
            });
        }
        
        if (linkedinBtn) {
            linkedinBtn.addEventListener('click', () => {
                const shareUrl = window.location.href;
                window.open(`https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(shareUrl)}`, '_blank');
            });
        }
        
        if (copyBtn) {
            copyBtn.addEventListener('click', () => {
                const shareUrl = window.location.href;
                navigator.clipboard.writeText(shareUrl).then(() => {
                    // Visual feedback for copy
                    const originalText = copyBtn.innerHTML;
                    copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                    
                    setTimeout(() => {
                        copyBtn.innerHTML = originalText;
                    }, 2000);
                });
            });
        }
    }
    
    // Event listener for analyze button
    if (analyzeButton) {
        analyzeButton.addEventListener("click", function () {
            if (doi) {
                getAnalysis(doi);
                
                // Button press animation
                gsap.to(this, {
                    duration: 0.1,
                    scale: 0.95,
                    onComplete: () => {
                        gsap.to(this, {
                            duration: 0.1,
                            scale: 1
                        });
                    }
                });
                
            } else {
                // Show error if DOI is missing
                const toast = document.createElement('div');
                toast.className = 'toast-notification error';
                toast.innerHTML = `
                    <i class="fas fa-exclamation-circle"></i>
                    <span>Error: DOI information is missing. Please try another paper.</span>
                `;
                
                document.body.appendChild(toast);
                
                // Animate toast in and out
                gsap.fromTo(toast, 
                    { y: -100, opacity: 0 },
                    { 
                        y: 20, 
                        opacity: 1, 
                        duration: 0.3,
                        onComplete: () => {
                            setTimeout(() => {
                                gsap.to(toast, {
                                    y: -100,
                                    opacity: 0,
                                    duration: 0.3,
                                    onComplete: () => toast.remove()
                                });
                            }, 3000);
                        }
                    }
                );
            }
        });
        
        // Button hover animations
        analyzeButton.addEventListener("mouseenter", function() {
            gsap.to(this, {
                duration: 0.3,
                y: -3,
                boxShadow: "0 8px 16px rgba(58, 134, 255, 0.4)"
            });
        });
        
        analyzeButton.addEventListener("mouseleave", function() {
            gsap.to(this, {
                duration: 0.3,
                y: 0,
                boxShadow: "0 6px 12px rgba(0, 0, 0, 0.2)"
            });
        });
    }
    
    // Download button animations
    const downloadButton = document.getElementById("btn-rs");
    if (downloadButton) {
        downloadButton.addEventListener("mouseenter", function() {
            gsap.to(this, {
                duration: 0.3,
                y: -3,
                boxShadow: "0 8px 16px rgba(0, 0, 0, 0.3)"
            });
        });
        
        downloadButton.addEventListener("mouseleave", function() {
            gsap.to(this, {
                duration: 0.3,
                y: 0,
                boxShadow: "0 6px 12px rgba(0, 0, 0, 0.2)"
            });
        });
        
        // Download button click effect
        downloadButton.addEventListener("click", function() {
            gsap.to(this, {
                duration: 0.1,
                scale: 0.95,
                onComplete: () => {
                    gsap.to(this, {
                        duration: 0.1,
                        scale: 1
                    });
                }
            });
        });
    }
    
    // Intersection Observer for revealing elements on scroll
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };
    
    const revealObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                revealObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe sections for reveal animations
    document.querySelectorAll('.paper-abstract, .metadata-card, .paper-badges').forEach(section => {
        section.classList.add('reveal-element');
        revealObserver.observe(section);
    });
    
    // Handle window resize events for responsive adjustments
    window.addEventListener('resize', debounce(function() {
        // Update any responsive elements if needed
        adjustMobileLayout();
    }, 250));
    
    // Adjust layout for mobile devices
    function adjustMobileLayout() {
        const windowWidth = window.innerWidth;
        
        if (windowWidth <= 768) {
            // Adjust for mobile layout if needed
            document.querySelectorAll('.metadata-item').forEach(item => {
                item.style.flexBasis = '100%';
            });
        } else {
            // Reset for larger screens
            document.querySelectorAll('.metadata-item').forEach(item => {
                item.style.flexBasis = '300px';
            });
        }
    }
    
    // Run initial layout adjustment
    adjustMobileLayout();
    
    // Add print functionality if needed
    const addPrintButton = () => {
        const paperActions = document.querySelector('.paper-actions');
        if (paperActions && analysisContent) {
            const printButton = document.createElement('button');
            printButton.className = 'action-button print-btn';
            printButton.innerHTML = '<i class="fas fa-print"></i> Print Analysis';
            
            printButton.addEventListener('click', () => {
                window.print();
            });
            
            // Add hover effects
            printButton.addEventListener("mouseenter", function() {
                gsap.to(this, {
                    duration: 0.3,
                    y: -3,
                    boxShadow: "0 8px 16px rgba(0, 0, 0, 0.3)"
                });
            });
            
            printButton.addEventListener("mouseleave", function() {
                gsap.to(this, {
                    duration: 0.3,
                    y: 0,
                    boxShadow: "0 6px 12px rgba(0, 0, 0, 0.2)"
                });
            });
            
            // Only add print button after analysis is shown
            const observer = new MutationObserver((mutations) => {
                if (analysisContent.classList.contains('visible') && !document.querySelector('.print-btn')) {
                    paperActions.appendChild(printButton);
                    
                    // Animate button entrance
                    gsap.from(printButton, {
                        duration: 0.5,
                        opacity: 0,
                        scale: 0.8,
                        ease: "back.out(1.7)"
                    });
                    
                    observer.disconnect();
                }
            });
            
            observer.observe(analysisContent, { attributes: true, attributeFilter: ['class'] });
        }
    };
    
    // Add print button functionality
    addPrintButton();
    
    // Utility function for debouncing
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Add toast notification styles dynamically
    const addToastStyles = () => {
        const styleElement = document.createElement('style');
        styleElement.textContent = `
            .toast-notification {
                position: fixed;
                top: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(30, 30, 50, 0.9);
                color: white;
                padding: 12px 24px;
                border-radius: 8px;
                z-index: 1000;
                display: flex;
                align-items: center;
                gap: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(131, 56, 236, 0.3);
            }
            
            .toast-notification.error {
                border-left: 4px solid #ff3366;
            }
            
            .toast-notification.success {
                border-left: 4px solid #00ffaa;
            }
            
            .toast-notification i {
                font-size: 18px;
            }
            
            .share-container {
                margin-top: 2rem;
                padding-top: 1.5rem;
                border-top: 1px solid rgba(131, 56, 236, 0.2);
            }
            
            .share-container h3 {
                font-size: 1.25rem;
                margin-bottom: 1rem;
                color: #f8f9fa;
            }
            
            .share-buttons {
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
            }
            
            .share-btn {
                padding: 8px 16px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 0.9rem;
                display: flex;
                align-items: center;
                gap: 8px;
                transition: all 0.3s ease;
                border: none;
                background: rgba(30, 30, 50, 0.6);
                color: #f8f9fa;
            }
            
            .share-btn:hover {
                transform: translateY(-2px);
            }
            
            .share-btn.twitter:hover {
                background: #1da1f2;
                color: white;
            }
            
            .share-btn.linkedin:hover {
                background: #0077b5;
                color: white;
            }
            
            .share-btn.copy:hover {
                background: #8338ec;
                color: white;
            }
            
            @media print {
                .navbar, .footer, .paper-actions, .share-container {
                    display: none !important;
                }
                
                body, .container {
                    background: white !important;
                    color: black !important;
                }
                
                .analysis-content {
                    max-height: none !important;
                    border: none !important;
                    box-shadow: none !important;
                }
            }
        `;
        document.head.appendChild(styleElement);
    };
    
    // Add toast styles
    addToastStyles();
});