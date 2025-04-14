document.addEventListener("DOMContentLoaded", function () {
    const searchButton = document.getElementById("btn-ls");
    const AnalysisContainer = document.querySelector(".analysis");
    const DOI = document.getElementById("res-doi").innerText.trim()
    const loadingSpinner = document.querySelector(".dyn-loading");
    const auth = document.getElementById("auth-token").innerText.trim();

    function showLoading() {
        loadingSpinner.style.display = "block"; 
        AnalysisContainer.style.display = "none"; 
    }

    function hideLoading() {
        loadingSpinner.style.display = "none"; 
        AnalysisContainer.style.display = "grid";
    }

    async function getAnalysis(doi) {

        showLoading();
        
        try {

            const response = await fetch('/analyze/', {
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
            }

            const msg = response;

            const data = await response.json();

        } catch (error) {

            console.error('Error Analyzing Paper',error);

            alert('Error Analyzing Paper. Please Try Again Later.');

        } finally {

            hideLoading(),5000
        }
    }
    
        
    searchButton.addEventListener("click", function () {
        if (DOI) {
            getAnalysis(DOI);
        } else {
            alert("Error!");
        }
    });
    
});

