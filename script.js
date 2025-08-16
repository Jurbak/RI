 window.onload = function() {
    initAutocomplete();

    // Ambil title dari dokumen
    let titleText = document.title; // contoh: "Chapter 1007 - Pendeta Kegilaan"

    // Cari angka setelah "Chapter"
    let match = titleText.match(/Chapter\s+(\d+)/i);
    let chapterNow = match ? match[1] : 1;

    // Set placeholder sesuai chapter
    document.getElementById("chapter-input").placeholder = "Chapter " + chapterNow;
    
    // Dark mode toggle
    const darkModeBtn = document.getElementById("darkModeBtn");
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
    }
    darkModeBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark-mode");
        localStorage.setItem("darkMode", document.body.classList.contains("dark-mode"));
    });
};


function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        
        window.onscroll = function() {
            let button = document.getElementById("scrollTopBtn");
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                button.style.display = "block";
            } else {
                button.style.display = "none";
            }
        };

        function initAutocomplete() {
            // Chapter navigation
            document.getElementById("go-btn").addEventListener("click", function() {
                goToChapter();
            });
            
            document.getElementById("chapter-input").addEventListener("keyup", function(event) {
                if (event.key === "Enter") {
                    goToChapter();
                }
            });
            
            // Setup autocomplete
            let input = document.getElementById("chapter-input");
            let currentValue = "";
            let chapters = [];
            
            // Generate chapter array (for larger novels, we might only show nearby chapters)
            for (let i = 1; i <= 2334; i++) {
                chapters.push("Chapter " + i);
            }
            
            input.addEventListener("input", function() {
                closeAllLists();
                
                if (!this.value) { return false; }
                currentValue = this.value;
                
                let container = document.createElement("DIV");
                container.setAttribute("id", this.id + "autocomplete-list");
                container.setAttribute("class", "autocomplete-items");
                
                this.parentNode.appendChild(container);
                
                // Filter chapters that match the input
                let matches = chapters.filter(item => 
                    item.toLowerCase().includes(currentValue.toLowerCase())
                );
                
                // Limit to first 10 matches for performance
                matches = matches.slice(0, 10);
                
                for (let i = 0; i < matches.length; i++) {
                    let item = document.createElement("DIV");
                    
                    // Highlight matching part
                    let matchIndex = matches[i].toLowerCase().indexOf(currentValue.toLowerCase());
                    if (matchIndex !== -1) {
                        item.innerHTML = matches[i].substr(0, matchIndex);
                        item.innerHTML += "<strong>" + matches[i].substr(matchIndex, currentValue.length) + "</strong>";
                        item.innerHTML += matches[i].substr(matchIndex + currentValue.length);
                    } else {
                        item.innerHTML = matches[i];
                    }
                    
                    item.innerHTML += "<input type='hidden' value='" + matches[i] + "'>";
                    
                    item.addEventListener("click", function() {
                        input.value = this.getElementsByTagName("input")[0].value;
                        closeAllLists();
                        goToChapter();
                    });
                    
                    container.appendChild(item);
                }
            });
            
            // Close lists when clicking elsewhere
            document.addEventListener("click", function(e) {
                closeAllLists(e.target);
            });
            
            function closeAllLists(elmnt) {
                let x = document.getElementsByClassName("autocomplete-items");
                for (let i = 0; i < x.length; i++) {
                    if (elmnt != x[i] && elmnt != input) {
                        x[i].parentNode.removeChild(x[i]);
                    }
                }
            }
        }
        
        function goToChapter() {
            let input = document.getElementById("chapter-input").value.trim().toLowerCase();
            let chapterNum = input.replace(/[^0-9]/g, "");
            
            if (chapterNum && !isNaN(chapterNum) && chapterNum >= 1 && chapterNum <= 2334) {
                window.location.href = "chapter_" + chapterNum + ".html";
            } else {
                alert("Please enter a valid chapter number (1-2334)");
            }
        }


