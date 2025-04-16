import requests
from bs4 import BeautifulSoup
import os
import time
import random
import glob
import re

# Base URL of the website to scrape
base_url = "https://meionovels.com/novel/pendeta-kegilaan/mtl/chapter-"
# Folder to save scraping results
output_folder = "chapter"
os.makedirs(output_folder, exist_ok=True)

# Create CSS file for better styling
css_folder = os.path.dirname(output_folder)
css_file_path = os.path.join(css_folder, "style.css")

# Check if CSS file exists, create if it doesn't
if not os.path.exists(css_file_path):
    with open(css_file_path, "w", encoding="utf-8") as css_file:
        css_file.write("""
/* Modern, clean styling for novel reading */
:root {
    --primary-color: #3498db;
    --bg-color: #f9f9f9;
    --text-color: #333;
    --nav-bg: #fff;
    --border-color: #ddd;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.8;
    color: var(--text-color);
    background-color: var(--bg-color);
    margin: 0;
    padding: 0;
}

.container {
    max-width: 800px;
    margin: 70px auto 30px;
    padding: 20px;
    background: white;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    border-radius: 5px;
}

h1 {
    color: var(--primary-color);
    text-align: center;
    padding-bottom: 10px;
    border-bottom: 1px solid var(--border-color);
}

p {
    margin-bottom: 1.2em;
    text-align: justify;
}

.top-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: var(--nav-bg);
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    z-index: 1000;
}

.nav-buttons {
    display: flex;
    gap: 10px;
    align-items: center;
}

.btn {
    display: inline-block;
    padding: 8px 15px;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 4px;
    transition: background-color 0.3s;
}

.btn:hover {
    background-color: #2980b9;
}

#chapter-input {
    padding: 8px;
    border: 1px solid var(--border-color);
    border-radius: 4px;
    width: 150px;
    font-size: 14px;
}

#chapter-input:focus {
    outline: 1px solid var(--primary-color);
    box-shadow: 0 0 3px rgba(52, 152, 219, 0.5);
}

.go-btn {
    padding: 8px 12px;
    background-color: var(--primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
}

.go-btn:hover {
    background-color: #2980b9;
}

#scrollTopBtn {
    display: none;
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: var(--primary-color);
    color: white;
    border: none;
    cursor: pointer;
    font-size: 18px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

#scrollTopBtn:hover {
    background-color: #2980b9;
}

/* Autocomplete container */
.autocomplete-container {
    position: relative;
    display: inline-block;
}

.autocomplete-items {
    position: absolute;
    border: 1px solid var(--border-color);
    border-top: none;
    z-index: 99;
    top: 100%;
    left: 0;
    right: 0;
    max-height: 200px;
    overflow-y: auto;
    background-color: white;
    border-radius: 0 0 4px 4px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.autocomplete-items div {
    padding: 8px 10px;
    cursor: pointer;
}

.autocomplete-items div:hover {
    background-color: #e9e9e9;
}

.autocomplete-active {
    background-color: var(--primary-color) !important;
    color: white;
}

/* Mobile responsive adjustments */
@media (max-width: 600px) {
    .container {
        margin-top: 60px;
        padding: 15px;
    }
    
    .top-nav {
        padding: 8px 10px;
    }
    
    .btn {
        padding: 6px 10px;
        font-size: 14px;
    }
    
    #chapter-input {
        width: 120px;
        padding: 6px;
    }
    
    .go-btn {
        padding: 6px 8px;
    }
}
""")
    print("CSS file created successfully.")
else:
    print("CSS file already exists.")

# Function to find missing chapters
def find_missing_chapters(folder_path, total_chapters):
    # Get list of all HTML files in the folder
    files = glob.glob(os.path.join(folder_path, "chapter_*.html"))
    
    # Extract chapter numbers from filenames
    chapter_numbers = []
    for file in files:
        # Use regex to extract number from filename
        match = re.search(r'chapter_(\d+)\.html', os.path.basename(file))
        if match:
            chapter_numbers.append(int(match.group(1)))
    
    # Sort the chapter numbers
    chapter_numbers.sort()
    
    # Find missing chapters (from 1 to total_chapters)
    missing_chapters = []
    for i in range(1, total_chapters + 1):
        if i not in chapter_numbers:
            missing_chapters.append(i)
    
    return missing_chapters, chapter_numbers

# Total number of chapters
total_chapters = 2334

# Check for missing chapters
print("Checking for missing chapters...")
missing_chapters, existing_chapters = find_missing_chapters(output_folder, total_chapters)

if not missing_chapters:
    print("All chapters are already downloaded. No need to download again.")
else:
    print(f"Found {len(missing_chapters)} missing chapters out of {total_chapters}.")
    print(f"First 10 missing chapters: {missing_chapters[:10]}")
    
    # Ask user if they want to continue
    user_input = input("Do you want to download missing chapters? (y/n): ").strip().lower()
    
    if user_input == 'y':
        print(f"Downloading {len(missing_chapters)} missing chapters...")
        
        # Loop through missing chapters only
        for chapter in missing_chapters:
            url = f"{base_url}{chapter}"
            
            try:
                # Add random delay to avoid getting blocked (1-3 seconds)
                time.sleep(random.uniform(1, 3))
                
                # Request with headers to mimic a browser
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
                }
                
                response = requests.get(url, headers=headers)
                
                # Check if page is accessible
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    
                    # Find content element (adjust according to the website's structure)
                    chapter_content = soup.find("div", class_="text-left")
                    
                    if chapter_content:
                        # Clean content - remove unwanted elements
                        for unwanted in chapter_content.find_all(["script", "iframe", "ins"]):
                            unwanted.decompose()
                        
                        # Navigation links
                        prev_page = f"chapter_{chapter-1}.html" if chapter > 1 else "#"
                        next_page = f"chapter_{chapter+1}.html" if chapter < total_chapters else "#"
                        
                        # Create HTML content with autocomplete input instead of dropdown
                        html_content = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter {chapter} - Pendeta Kegilaan</title>
    <link rel="stylesheet" href="../style.css">
    <script>
        function scrollToTop() {{
            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}
        
        window.onscroll = function() {{
            let button = document.getElementById("scrollTopBtn");
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {{
                button.style.display = "block";
            }} else {{
                button.style.display = "none";
            }}
        }};

        function initAutocomplete() {{
            // Chapter navigation
            document.getElementById("go-btn").addEventListener("click", function() {{
                goToChapter();
            }});
            
            document.getElementById("chapter-input").addEventListener("keyup", function(event) {{
                if (event.key === "Enter") {{
                    goToChapter();
                }}
            }});
            
            // Setup autocomplete
            let input = document.getElementById("chapter-input");
            let currentValue = "";
            let chapters = [];
            
            // Generate chapter array (for larger novels, we might only show nearby chapters)
            for (let i = 1; i <= {total_chapters}; i++) {{
                chapters.push("Chapter " + i);
            }}
            
            input.addEventListener("input", function() {{
                closeAllLists();
                
                if (!this.value) {{ return false; }}
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
                
                for (let i = 0; i < matches.length; i++) {{
                    let item = document.createElement("DIV");
                    
                    // Highlight matching part
                    let matchIndex = matches[i].toLowerCase().indexOf(currentValue.toLowerCase());
                    if (matchIndex !== -1) {{
                        item.innerHTML = matches[i].substr(0, matchIndex);
                        item.innerHTML += "<strong>" + matches[i].substr(matchIndex, currentValue.length) + "</strong>";
                        item.innerHTML += matches[i].substr(matchIndex + currentValue.length);
                    }} else {{
                        item.innerHTML = matches[i];
                    }}
                    
                    item.innerHTML += "<input type='hidden' value='" + matches[i] + "'>";
                    
                    item.addEventListener("click", function() {{
                        input.value = this.getElementsByTagName("input")[0].value;
                        closeAllLists();
                        goToChapter();
                    }});
                    
                    container.appendChild(item);
                }}
            }});
            
            // Close lists when clicking elsewhere
            document.addEventListener("click", function(e) {{
                closeAllLists(e.target);
            }});
            
            function closeAllLists(elmnt) {{
                let x = document.getElementsByClassName("autocomplete-items");
                for (let i = 0; i < x.length; i++) {{
                    if (elmnt != x[i] && elmnt != input) {{
                        x[i].parentNode.removeChild(x[i]);
                    }}
                }}
            }}
        }}
        
        function goToChapter() {{
            let input = document.getElementById("chapter-input").value.trim().toLowerCase();
            let chapterNum = input.replace(/[^0-9]/g, "");
            
            if (chapterNum && !isNaN(chapterNum) && chapterNum >= 1 && chapterNum <= {total_chapters}) {{
                window.location.href = "chapter_" + chapterNum + ".html";
            }} else {{
                alert("Please enter a valid chapter number (1-{total_chapters})");
            }}
        }}
        
        // Initialize when page loads
        window.onload = function() {{
            initAutocomplete();
            // Pre-set the current chapter
            document.getElementById("chapter-input").placeholder = "Chapter {chapter}";
        }};
    </script>
</head>
<body>
    <div class="top-nav">
        <a href="{prev_page}" class="btn" {' style="visibility:hidden;"' if chapter == 1 else ""}>« Prev</a>
        
        <div class="autocomplete-container">
            <input id="chapter-input" type="text" placeholder="Chapter {chapter}">
            <button id="go-btn" class="go-btn">Go</button>
        </div>
        
        <a href="{next_page}" class="btn" {' style="visibility:hidden;"' if chapter == total_chapters else ""}>Next »</a>
    </div>
    
    <div class="container">
        <h1>Chapter {chapter}</h1>
        {chapter_content}
    </div>
    
    <button id="scrollTopBtn" onclick="scrollToTop()">↑</button>
</body>
</html>"""
                        
                        # Save to HTML file
                        file_path = os.path.join(output_folder, f"chapter_{chapter}.html")
                        with open(file_path, "w", encoding="utf-8") as file:
                            file.write(html_content)
                        
                        print(f"Chapter {chapter} saved successfully!")
                    else:
                        print(f"Chapter {chapter} has no content.")
                else:
                    print(f"Failed to access Chapter {chapter}, status code: {response.status_code}")
            
            except Exception as e:
                print(f"Error processing Chapter {chapter}: {str(e)}")
                # Continue with next chapter instead of stopping
                continue
        
        print("Download of missing chapters completed!")
        
        # Check again after downloading
        final_missing, final_existing = find_missing_chapters(output_folder, total_chapters)
        if final_missing:
            print(f"There are still {len(final_missing)} chapters missing.")
            print(f"First 10 still missing: {final_missing[:10]}")
        else:
            print("All chapters have been downloaded successfully!")
    else:
        print("Download canceled by user.")

# Function to create an index.html file with chapter list
def create_index_file():
    print("Creating index.html file...")
    
    # Get all available chapters
    _, available_chapters = find_missing_chapters(output_folder, total_chapters)
    
    # Create HTML content for index file
    html_content = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pendeta Kegilaan - Chapter List</title>
    <link rel="stylesheet" href="style.css">
    <style>
        .chapter-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            margin-top: 20px;
        }
        
        .chapter-link {
            display: block;
            padding: 10px;
            background-color: #f5f5f5;
            border-radius: 4px;
            text-align: center;
            text-decoration: none;
            color: var(--text-color);
            transition: all 0.2s ease;
        }
        
        .chapter-link:hover {
            background-color: var(--primary-color);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        h1 {
            margin-bottom: 20px;
        }
        
        .search-container {
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
        }
        
        #chapter-search {
            flex: 1;
            padding: 10px;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            font-size: 16px;
        }
        
        .status-box {
            background-color: #f0f0f0;
            border-radius: 4px;
            padding: 15px;
            margin-bottom: 20px;
        }
        
        .missing {
            color: #e74c3c;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Pendeta Kegilaan - Chapter List</h1>
"""
    
    # Calculate status info
    missing_count = total_chapters - len(available_chapters)
    percentage_complete = (len(available_chapters) / total_chapters) * 100
    
    # Add status box
    html_content += f"""
        <div class="status-box">
            <p><strong>Total Chapters:</strong> {total_chapters}</p>
            <p><strong>Available Chapters:</strong> {len(available_chapters)}</p>
            <p><strong>Missing Chapters:</strong> <span class="{'missing' if missing_count > 0 else ''}">{missing_count}</span></p>
            <p><strong>Completion:</strong> {percentage_complete:.1f}%</p>
        </div>
        
        <div class="search-container">
            <input type="text" id="chapter-search" placeholder="Search for chapter..." onkeyup="filterChapters()">
        </div>
        
        <div class="chapter-grid" id="chapter-grid">
"""
    
    # Add links for all chapters
    for i in range(1, total_chapters + 1):
        available = i in available_chapters
        html_content += f"""            <a href="{'chapter/chapter_' + str(i) + '.html' if available else '#'}" 
               class="chapter-link" 
               data-chapter="{i}"
               {' style="opacity: 0.5; pointer-events: none;"' if not available else ''}>
                Chapter {i}{'' if available else ' (Missing)'}
            </a>
"""
    
    # Close tags and add search script
    html_content += """        </div>
    </div>
    
    <script>
        function filterChapters() {
            let input = document.getElementById("chapter-search");
            let filter = input.value.toLowerCase();
            let grid = document.getElementById("chapter-grid");
            let links = grid.getElementsByTagName("a");
            
            for (let i = 0; i < links.length; i++) {
                let chapter = links[i].getAttribute("data-chapter");
                if (chapter.includes(filter)) {
                    links[i].style.display = "";
                } else {
                    links[i].style.display = "none";
                }
            }
        }
    </script>
</body>
</html>"""
    
    # Save the index file
    with open(os.path.join(css_folder, "index.html"), "w", encoding="utf-8") as file:
        file.write(html_content)
    
    print("Index file created successfully!")

# Create index file at the end
create_index_file()

print("All operations completed successfully!")