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
        
        try{
        /*try {
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
                      
            const data = await response.json();*/
    
            searchTitle.textContent = `Search Results for : ${query}`;
            
            scrapItemsContainer.innerHTML = '';

            data = [
                {
                    'title': 'Artificial Intelligence and Augmented Reality Exploration',
                    'authors' : 'Ian GodFellow',
                    'date' : 'April 2025',
                    'doi' : 'arXiv/2540.4250',
                    'field': 'Artificial Intelligence, Computational Theory',
                    'abstract': 'Artificial Intelligence is the method of training computational systems to perform great tasks in the environment.',
                    'link' : 'https://127.0.0.1:5425/paper/rttXpyuiop'
                },
                {
                    'title': 'Artificial Intelligence',
                    'authors' : 'Ian GodFellow',
                    'Year' : 'April 2025',
                    'doi' : 'arXiv/2540.4250',
                    'field': 'Artificial Intelligence, Computational Theory',
                    'abstract': 'Artificial Intelligence is the method of training computational systems to perform great tasks in the environment.',
                    'link' : 'https://127.0.0.1:5425/paper/rttXpyuiop'
                },
            ]
    
            data.forEach((item) => {
                const itemElement = document.createElement('div');
                itemElement.classList.add('dyn-scrap-item');
    
                itemElement.innerHTML = `
                    <img src="../assets/img/dynax.svg">
                    <h3>${item.title?.slice(0, 100) || "No Title"}</h3>

                    <div class="info-line"><strong> Authors: </strong> ${item.authors} </div>
                    <div class="info-line"><strong> Year: </strong> ${item.date} </div>
                    <div class="info-line"><strong> DOI: </strong> ${item.doi} </div>
                    <div class="info-line"><strong> Journal: </strong> ${item.field} </div>
                    <div class="info-line"><strong> Abstract: </strong> ${item.abstract} </div>

                    <div class="metadata">
                        <a href="${item.link}" target="_blank"> Explore → </a>
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

