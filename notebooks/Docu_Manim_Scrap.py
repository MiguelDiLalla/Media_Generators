import os
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from urllib.parse import urljoin
from tqdm import tqdm
import time
import json

# Detect if the environment is Google Colab or local
try:
    from google.colab import drive
    COLAB_ENV = True
except ImportError:
    COLAB_ENV = False

# Base URL of the Manim documentation
BASE_URL = "https://docs.manim.community/en/stable/reference.html"

# Set output directory based on environment
if COLAB_ENV:
    OUTPUT_DIR = "/content/manim_docs"
else:
    OUTPUT_DIR = os.path.join(os.getcwd(), "manim_docs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# File to track downloaded links
PROGRESS_FILE = os.path.join(OUTPUT_DIR, "progress.json")

# Maximum depth for scraping
MAX_DEPTH = 2

# Load or initialize progress tracking
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, "r") as file:
            return json.load(file)
    return {"downloaded": [], "visited": []}

def save_progress(progress):
    with open(PROGRESS_FILE, "w") as file:
        json.dump(progress, file)

def get_links(base_url, current_depth):
    """
    Collects all unique links from the given page up to a specified depth.

    Args:
        base_url (str): The base URL of the documentation.
        current_depth (int): Current depth of scraping.

    Returns:
        list: A list of unique absolute URLs found on the page.
    """
    if current_depth > MAX_DEPTH:
        return []

    response = requests.get(base_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch {base_url}: {response.status_code}")

    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        url = urljoin(base_url, a_tag['href'])
        if "https://docs.manim.community/en/stable/" in url:
            links.append(url)
    return list(set(links))  # Remove duplicates

def make_links_absolute(html_content, base_url):
    """
    Converts all relative links in the HTML content to absolute URLs.

    Args:
        html_content (str): The HTML content as a string.
        base_url (str): The base URL to resolve relative links.

    Returns:
        str: The updated HTML content with absolute links.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    for tag in soup.find_all(['a', 'img'], href=True):
        tag['href'] = urljoin(base_url, tag['href'])
    for tag in soup.find_all('img', src=True):
        tag['src'] = urljoin(base_url, tag['src'])
    return str(soup)

def download_page(url, output_dir, progress):
    """
    Downloads the content of a given URL and saves it as an HTML file.

    Args:
        url (str): The URL to download.
        output_dir (str): The directory to save the HTML file.
        progress (dict): The progress tracker dictionary.

    Returns:
        str: The file path of the saved HTML file, or None if the download fails.
    """
    try:
        # Skip if already downloaded
        if url in progress["downloaded"]:
            return None

        response = requests.get(url)
        if response.status_code == 200:
            # Convert links to absolute for proper functionality
            html_content = make_links_absolute(response.text, url)
            file_name = url.split('/')[-1] or "index.html"
            file_path = os.path.join(output_dir, f"{file_name}.html")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_content)
            progress["downloaded"].append(url)
            save_progress(progress)
            return file_path
        else:
            print(f"Failed to download {url}: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    return None

def html_to_pdf(html_files, output_pdf):
    """
    Converts a list of HTML files into a single PDF file.

    Args:
        html_files (list): List of file paths to HTML files.
        output_pdf (str): The path to the output PDF file.
    """
    pdf_pages = []
    for html_file in tqdm(html_files, desc="Rendering HTML to PDF"):
        try:
            pdf_pages.append(HTML(html_file).render())
        except Exception as e:
            print(f"Error rendering {html_file}: {e}")
    if pdf_pages:
        combined_pdf = pdf_pages[0]
        for page in pdf_pages[1:]:
            combined_pdf.pages.extend(page.pages)
        combined_pdf.write_pdf(output_pdf)
        print(f"Final PDF generated: {output_pdf}")
    else:
        print("No PDF pages were generated.")

def main():
    """
    Main function to scrape the Manim documentation and export it as a PDF.
    """
    try:
        # Step 1: Collect all relevant links
        print("Collecting links from the documentation...")
        progress = load_progress()
        if "visited" not in progress:
            progress["visited"] = []

        links_to_visit = [BASE_URL]
        all_links = set()

        for depth in range(1, MAX_DEPTH + 1):
            new_links = []
            for link in links_to_visit:
                if link not in progress["visited"]:
                    progress["visited"].append(link)
                    save_progress(progress)
                    new_links.extend(get_links(link, depth))
            all_links.update(new_links)
            links_to_visit = new_links

        print(f"Found {len(all_links)} links within depth {MAX_DEPTH}.")

        # Step 2: Download all pages with a progress bar
        print("Downloading pages...")
        html_files = []
        for link in tqdm(all_links, desc="Downloading HTML pages"):
            file_path = download_page(link, OUTPUT_DIR, progress)
            if file_path:
                html_files.append(file_path)
            time.sleep(0.5)  # Adjusted limit

        # Step 3: Convert HTML files to a single PDF
        print("Generating PDF...")
        pdf_path = os.path.join(OUTPUT_DIR, "manim_docs_complete.pdf")
        html_to_pdf([os.path.join(OUTPUT_DIR, f) for f in os.listdir(OUTPUT_DIR) if f.endswith('.html')], pdf_path)

        # Step 4: Handle output for Colab
        if COLAB_ENV:
            from google.colab import files
            print("Downloading PDF to local machine...")
            files.download(pdf_path)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if COLAB_ENV:
        print("Running in Google Colab environment.")
    else:
        print("Running in local environment.")
    main()
