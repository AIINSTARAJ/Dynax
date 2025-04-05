document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("search-bar");
    const searchButton = document.getElementById("search-btn");
    const scrapItemsContainer = document.querySelector(".dyn-scrap-items");
    const loadingSpinner = document.querySelector(".dyn-loading");
    const searchTitle = document.getElementById("dyn-search-title");

    function showLoading() {
        loadingSpinner.style.display = "block"; 
        scrapItemsContainer.style.display = "none"; 
        searchTitle.innerHTML = ''
    }

    function hideLoading() {
        loadingSpinner.style.display = "none"; 
        scrapItemsContainer.style.display = "grid";
    }

    async function fetchResearchPapers(query) {

        showLoading();
    
        try {
            const response = await fetch('/scrap', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 'message': query }),
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const data = await response.json();
    
            searchTitle.textContent = `Search Results for: ${query}`;
            
            scrapItemsContainer.innerHTML = '';
    
            data.forEach((item) => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('dyn-scrap-item');
    
                itemElement.innerHTML = `
                    <img src="../assets/img/dynax.svg">
                    <h3>${item.title}</h3>
                    <p><strong>Authors:</strong> ${item.authors}</p>
                    <p id='dyn-abs'><strong>Abstract:</strong> ${item.abstract}</p>
                    <div class="metadata">
                        <span><a id='dyn-link' href="${item.url}" target="_blank">Read more →</a></span>
                    </div>
                `;
    
                scrapItemsContainer.appendChild(itemElement);
            });
        } catch (error) {

            console.error('Error fetching research papers:', error);
            alert('Failed to fetch research papers. Please try again later.',error);

        } finally {
            hideLoading();
        }
    }
    
        
    searchButton.addEventListener("click", function () {
        const query = searchInput.value.trim();

        if (query) {
            fetchResearchPapers(query);
        } else {
            alert("Please enter a search query!");
        }
    });
    
    searchInput.addEventListener("keypress", function (e) {
        if (e.key === "Enter") {
            const query = searchInput.value.trim();

            if (query) {
                fetchResearchPapers(query);
            } else {
                alert("Please enter a search query!");
            }
        }
    });
});

