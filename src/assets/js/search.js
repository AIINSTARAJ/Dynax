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
  
        setTimeout(async function () {
            
            const data = [
                {
                    title: "Research Paper 1",
                    author: "Author A, Author B",
                    abstract: "This paper discusses machine learning applications in AI.",
                    link: "#",
                },
                {
                    title: "Research Paper 2",
                    author: "Author C, Author D",
                    abstract: "This paper explores deep learning in neural networks.",
                    link: "#",
                },
                {
                    title: "Research Paper 3",
                    author: "Author E, Author F",
                    abstract: "This paper presents a survey on AI and robotics.",
                    link: "#",
                },
                {
                    title: "Research Paper 4",
                    author: "Author G, Author H",
                    abstract: "This paper talks about computer vision and AI ethics.",
                    link: "#",
                },
                {
                    title: "Research Paper 5",
                    author: "Author I, Author J",
                    abstract: "This paper explores Retreival Augmented Generation.",
                    link: "#",
                },
                {
                    title: "Research Paper 6",
                    author: "Author K, Author L",
                    abstract: "This paper introduces LangChain and LLM.",
                    link: "#",
                },
            ];
            searchTitle.textContent = "Search Results for : ".concat(query);

            scrapItemsContainer.innerHTML = "";

            data.forEach((item) => {

                const itemElement = document.createElement("div");
                itemElement.classList.add("dyn-scrap-item");


                itemElement.innerHTML = `
                    <img src="../assets/img/dynax.svg">
                    <h3> ${item.title} </h3>
                    <p><strong> Authors: </strong> ${item.author} </p>
                    <p id='dyn-abs'><strong> Abstract: </strong> ${item.abstract} </p>
                    <div class="metadata">
                        <span><a id='dyn-link' href="${item.link}" target="_blank"> Read more → </a></span>
                    </div>
                `;

                scrapItemsContainer.appendChild(itemElement);
            });

            hideLoading();}, 1000);
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

