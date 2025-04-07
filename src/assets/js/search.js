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

            const msg = response;

            if (msg === "Error! Network Failure" || msg === 'Error! Unauthorized Access')

                alert("Error in Scraping Research Papers")                                
                      
            const data = await response.json();
    
            searchTitle.textContent = `Search Results for : ${query}`;
            
            scrapItemsContainer.innerHTML = '';
    
            data.forEach((item) => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('dyn-scrap-item');
    
                itemElement.innerHTML = `
                    <img src="../assets/img/dynax.svg">
                    <h3>${item.title?.slice(0, 100) || "No Title"}</h3>

                    <div class="info-line"><strong> Authors: </strong> ${item.authors}</div>
                    <div class="info-line"><strong> Year: </strong> ${item.year}</div>
                    <div class="info-line"><strong> Citations: </strong> ${item.citations}</div>
                    <div class="info-line"><strong> Publisher: </strong> ${item.publisher}</div>
                    <div class="info-line"><strong> DOI: </strong> ${item.doi}</div>
                    <div class="info-line"><strong> Journal: </strong> ${item.publication}</div>
                    <div class="info-line"><strong> Type: </strong> ${item.journal_type}</div>

                    <div class="metadata">
                        <a href="${item.url}" target="_blank">View Full Paper</a>
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

