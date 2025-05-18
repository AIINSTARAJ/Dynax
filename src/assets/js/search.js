document.addEventListener("DOMContentLoaded", function () {
    // DOM Elements //Logic
    const searchInput = document.getElementById("search-bar");
    const searchButton = document.getElementById("search-btn");
    const searchTags = document.querySelectorAll(".search-tag");
    const resultsContainer = document.querySelector(".search-results-container");
    const loadingContainer = document.querySelector(".loading-container");
    const searchResultsSection = document.querySelector(".search-results-section");
    const noResultsSection = document.querySelector(".no-results-section");
    const searchResultsTitle = document.getElementById("search-results-title");
    const resultsCountElement = document.getElementById("results-count");
    const loadMoreButton = document.getElementById("load-more");
    const filterOptions = document.querySelectorAll(".filter-option");
    const currentSortDisplay = document.getElementById("current-sort");
    const filterDropdown = document.querySelector(".filter-dropdown");
    const filterBtn = document.querySelector(".filter-btn");
    const popularSearches = document.querySelector(".popular-searches");
    const searchSuggestions = document.querySelector(".search-suggestions");
    
    // Search state
    let currentPage = 1;
    let currentQuery = "";
    let currentSort = "relevance";
    let hasMoreResults = false;
    let isSearching = false;
    let searchDebounceTimer;
    let suggestionsList = [];
    let totalResults = 0;
    let resultsPerPage = 50; // Setting initial page size to 50
    let allResults = []; // Store all fetched results
    let displayedResults = 0; // Track number of displayed results

    // Animation for search hero section
    function setupSearchAnimation() {
        const text = "Discover groundbreaking research papers";
        const typingEffect = document.querySelector(".typing-effect");
        typingEffect.textContent = "";
        
        let i = 0;
        const typeInterval = setInterval(() => {
            if (i < text.length) {
                typingEffect.textContent += text.charAt(i);
                i++;
            } else {
                clearInterval(typeInterval);
                
                // Add cursor blink animation after typing completes
                typingEffect.classList.add("cursor-blink");
            }
        }, 150);
    }

    // Initialize UI
    function init() {
        setupSearchAnimation();
        searchResultsSection.style.display = "none";
        noResultsSection.style.display = "none";
        loadingContainer.style.display = "none";
        
        // Setup event listeners
        setupEventListeners();
        
        // Setup filter dropdown animation
        setupFilterDropdown();
        
        // Handle query parameters if any
        const urlParams = new URLSearchParams(window.location.search);
        const queryParam = urlParams.get('q');
        
        if (queryParam) {
            searchInput.value = queryParam;
            executeSearch(queryParam);
        }
    }

    // Setup all event listeners
    function setupEventListeners() {
        // Search button click
        searchButton.addEventListener("click", function() {
            handleSearchSubmit();
        });
        
        // Enter key in search input
        searchInput.addEventListener("keypress", function(e) {
            if (e.key === "Enter") {
                handleSearchSubmit();
            }
        });
        
        // Input changes for search suggestions
        searchInput.addEventListener("input", handleSearchInput);
        
        // Focus/blur events for search input
        searchInput.addEventListener("focus", function() {
            if (suggestionsList.length > 0) {
                searchSuggestions.style.display = "block";
            }
        });
        
        // Document click to hide suggestions
        document.addEventListener("click", function(e) {
            if (!searchInput.contains(e.target) && !searchSuggestions.contains(e.target)) {
                searchSuggestions.style.display = "none";
            }
        });
        
        // Search tag clicks
        searchTags.forEach(tag => {
            tag.addEventListener("click", function() {
                const query = this.getAttribute("data-query");
                searchInput.value = query;
                executeSearch(query);
            });
        });
        
        // Load more results
        loadMoreButton.addEventListener("click", function() {
            if (!isSearching) {
                loadMoreResults();
            }
        });
        
        // Filter options
        filterOptions.forEach(option => {
            option.addEventListener("click", function() {
                const newSort = this.getAttribute("data-sort");
                if (newSort !== currentSort) {
                    currentSort = newSort;
                    currentSortDisplay.textContent = this.textContent;
                    currentPage = 1;
                    executeSearch(currentQuery, true);
                }
                document.querySelector(".filter-options").classList.remove("active");
            });
        });
    }

    // Setup filter dropdown behavior
    function setupFilterDropdown() {
        filterBtn.addEventListener("click", function() {
            document.querySelector(".filter-options").classList.toggle("active");
        });
        
        // Close dropdown when clicking outside
        document.addEventListener("click", function(e) {
            if (!filterDropdown.contains(e.target)) {
                document.querySelector(".filter-options").classList.remove("active");
            }
        });
    }

    // Handle search input changes
    function handleSearchInput() {
        const query = searchInput.value.trim();
        
        // Clear previous debounce timer
        clearTimeout(searchDebounceTimer);
        
        if (query.length < 2) {
            searchSuggestions.style.display = "none";
            return;
        }
        
        // Debounce search suggestions
        searchDebounceTimer = setTimeout(() => {
            fetchSearchSuggestions(query);
        }, 300);
    }

    // Fetch search suggestions from API
    function fetchSearchSuggestions(query) {
        // This would be replaced with your actual API call
        // For now, we'll use a mock implementation
        const mockSuggestions = [
            `${query}`,
        ];
        
        updateSearchSuggestions(mockSuggestions);
    }

    // Update search suggestions UI
    function updateSearchSuggestions(suggestions) {
        suggestionsList = suggestions;
        
        if (suggestions.length === 0) {
            searchSuggestions.style.display = "none";
            return;
        }
        
        searchSuggestions.innerHTML = "";
        suggestions.forEach(suggestion => {
            const item = document.createElement("div");
            item.classList.add("suggestion-item");
            item.textContent = suggestion;
            
            item.addEventListener("click", function() {
                searchInput.value = suggestion;
                searchSuggestions.style.display = "none";
                handleSearchSubmit();
            });
            
            searchSuggestions.appendChild(item);
        });
        
        if (document.activeElement === searchInput) {
            searchSuggestions.style.display = "block";
        }
    }

    // Handle search submission
    function handleSearchSubmit() {
        const query = searchInput.value.trim();
        if (query && !isSearching) {
            executeSearch(query);
            
            // Update URL with search query
            const url = new URL(window.location);
            url.searchParams.set('q', query);
            window.history.pushState({}, '', url);
        } else if (!query) {
            showToast("Please enter a search term");
        }
    }

    // Show toast notification
    function showToast(message) {
        // Create toast element if it doesn't exist
        let toast = document.querySelector(".toast-notification");
        if (!toast) {
            toast = document.createElement("div");
            toast.classList.add("toast-notification");
            document.body.appendChild(toast);
        }
        
        toast.textContent = message;
        toast.classList.add("show");
        
        setTimeout(() => {
            toast.classList.remove("show");
        }, 3000);
    }

    // Execute search
    async function executeSearch(query, resetResults = true) {
        // Don't allow multiple concurrent searches
        if (isSearching) return;
        
        isSearching = true;
        currentQuery = query;
        
        // Reset UI for new search
        if (resetResults) {
            resultsContainer.innerHTML = "";
            currentPage = 1;
            allResults = [];
            displayedResults = 0;
            
            // Scroll to top if not already there
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }
        
        // Show loading state
        searchResultsSection.style.display = "none";
        noResultsSection.style.display = "none";
        loadingContainer.style.display = "flex";
        popularSearches.style.display = "none";
        
        try {
            // Make API request
            const data = await fetchResearchPapers(query);
            
            // Update UI based on results
            if (resetResults) {
                allResults = data;
                totalResults = data.length;
            } else {
                allResults = [...allResults, ...data];
                totalResults = allResults.length;
            }
            
            updateSearchResults(data, resetResults);
        } catch (error) {
            console.error('Error executing search:', error);
            showToast('Search failed. Please try again later.');
            
            loadingContainer.style.display = "none";
            searchResultsSection.style.display = "none";
            noResultsSection.style.display = "flex";
        } finally {
            isSearching = false;
        }
    }

    // Fetch research papers from API
    async function fetchResearchPapers(query) {
        try {
            // Simulate network delay for demonstration
            await new Promise(resolve => setTimeout(resolve, 1500));
            
            // This would be your actual API call
            const response = await fetch('/scrap', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    'message': query,
                    'sort': currentSort,
                    'max': 200
                }),
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            
            const data = await response.json();
            return data;
            
        } catch (error) {
            console.error('Error fetching research papers:', error);
            throw error;
        }
    }

    // Update search results UI
    function updateSearchResults(data, resetResults) {
        loadingContainer.style.display = "none";
        
        if (!data || data.length === 0) {
            searchResultsSection.style.display = "none";
            noResultsSection.style.display = "flex";
            return;
        }
        
        // Show results section
        searchResultsSection.style.display = "block";
        noResultsSection.style.display = "none";
        
        // Determine how many results to display initially
        const resultsToDisplay = resetResults ? Math.min(data.length, resultsPerPage) : data.length;
        
        // Update results title and count
        searchResultsTitle.textContent = `Results for "${currentQuery}"`;
        
        if (resetResults) {
            // First batch of results
            resultsCountElement.textContent = `Showing 1 - ${resultsToDisplay} of ${totalResults} results`;
        } else {
            // Additional results
            resultsCountElement.textContent = `Showing 1 - ${displayedResults + resultsToDisplay} of ${totalResults} results`;
        }
        
        // Display only the first batch of results if this is a new search
        const displayData = resetResults ? data.slice(0, resultsPerPage) : data;
        
        // Append results to container
        displayData.forEach((item, index) => {
            // Create result card with animation delay
            const resultCard = document.createElement('div');
            resultCard.classList.add('result-card');
            resultCard.style.animationDelay = `${index * 0.1}s`;
            
            // Format abstract for display (truncate if needed)
            const abstract = item.abstract ? item.abstract.substring(0, 600) + (item.abstract.length > 600 ? '...' : '') : 'No abstract available';
            
            resultCard.innerHTML = `
                <div class="result-content">
                    <h3 class="result-title">${item.title}</h3>
                    <div class="result-meta">
                        <div class="result-authors">
                            <i class="fas fa-users"></i> ${item.authors || 'Unknown Authors'}
                        </div>
                        <div class="result-date">
                            <i class="fas fa-calendar-alt"></i> ${item.date || 'Date unknown'}
                        </div>
                        <div class="result-field">
                            <i class="fas fa-tag"></i> ${item.field || 'General'}
                        </div>
                    </div>
                    <div class="result-abstract">
                        <div>${item.abstract}</div>
                    </div>
                    <div class="result-footer">
                        ${item.doi ? `<div class="result-doi"><strong>DOI:</strong> ${item.doi}</div>` : ''}
                        <a href="${item.link}" target="_blank" class="view-paper-btn">
                            <span>View Paper</span>
                            <i class="fas fa-external-link-alt"></i>
                        </a>
                    </div>
                </div>
            `;
            
            resultsContainer.appendChild(resultCard);
        });
        
        // Update displayed results count
        displayedResults += resultsPerPage;
        
        // Update load more button visibility
        hasMoreResults = displayedResults < totalResults;
        loadMoreButton.style.display = hasMoreResults ? "flex" : "none";
        
        // Update load more button text
        if (hasMoreResults) {
            const remaining = totalResults - displayedResults;
            loadMoreButton.innerHTML = `<span>Load ${remaining} More Results</span> <i class="fas fa-chevron-down"></i>`;
        }
    }
    
    // Load more results from already fetched data
    function loadMoreResults() {
        if (displayedResults >= totalResults) {
            loadMoreButton.style.display = "none";
            return;
        }
        
        // Determine remaining results to display
        const remainingToDisplay = allResults.slice(displayedResults);
        
        // Update the results container with the remaining results
        updateSearchResults(remainingToDisplay, false);
    }

    // Initialize the page
    init();
});