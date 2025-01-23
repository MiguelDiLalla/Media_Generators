import os
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from urllib.parse import urljoin

# URL base de la documentación
BASE_URL = "https://docs.manim.community/en/stable/reference.html"

# Crear directorio para almacenar las páginas descargadas
os.makedirs("manim_docs", exist_ok=True)

def get_links(base_url):
    """Recoge todos los enlaces de la página principal."""
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        url = urljoin(base_url, a_tag['href'])
        if "https://docs.manim.community/en/stable/" in url:
            links.append(url)
    return list(set(links))  # Evitar duplicados

def download_page(url, output_dir):
    """Descarga el contenido HTML de una URL y lo guarda."""
    response = requests.get(url)
    if response.status_code == 200:
        file_name = url.split('/')[-1] or "index.html"
        file_path = os.path.join(output_dir, f"{file_name}.html")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(response.text)
        print(f"Guardado: {file_path}")
        return file_path
    else:
        print(f"Error al descargar {url}: {response.status_code}")
        return None

def html_to_pdf(html_files, output_pdf):
    """Convierte archivos HTML en un único PDF."""
    pdf_pages = []
    for html_file in html_files:
        pdf_pages.append(HTML(html_file).render())
    combined_pdf = pdf_pages[0]
    for page in pdf_pages[1:]:
        combined_pdf.pages.extend(page.pages)
    combined_pdf.write_pdf(output_pdf)
    print(f"PDF final generado: {output_pdf}")

def main():
    # Obtener todos los enlaces relevantes
    print("Recogiendo enlaces...")
    links = get_links(BASE_URL)
    print(f"Encontrados {len(links)} enlaces.")

    # Descargar todas las páginas
    print("Descargando páginas...")
    html_files = []
    for link in links:
        file_path = download_page(link, "manim_docs")
        if file_path:
            html_files.append(file_path)

    # Convertir HTML a PDF
    print("Generando PDF...")
    html_to_pdf(html_files, "manim_docs_complete.pdf")

if __name__ == "__main__":
    main()
