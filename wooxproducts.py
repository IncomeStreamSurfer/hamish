import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def extract_product_info(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the body content, assuming the first one is the main product description
        body_tag = soup.find('div', attrs={'data-pf-type': 'Body'})
        body_content = body_tag.get_text(separator=' ', strip=True) if body_tag else None

        return body_content
    except Exception as e:
        return None

def extract_sitemap_data(xml_file_path, search_terms, num_urls=20):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    namespaces = {
        'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'image': 'http://www.google.com/schemas/sitemap-image/1.1'
    }

    products = []
    for url in tqdm(root.findall('ns:url', namespaces), desc="Processing URLs"):
        if len(products) >= num_urls:
            break

        loc = url.find('ns:loc', namespaces).text
        image = url.find('image:image', namespaces)
        if image is not None and any(term.lower() in loc.lower() for term in search_terms):
            image_loc = image.find('image:loc', namespaces).text
            body_content = extract_product_info(loc)
            if body_content:  # Skip products with no body content
                products.append((loc, image_loc, body_content))

    return products

def main():
    xml_file_path = 'sitemap_products_13.xml'  # Replace with your XML file path
    search_terms = ['axe']  # Replace with your search terms
    random_entries = extract_sitemap_data(xml_file_path, search_terms)

    for entry in tqdm(random_entries, desc="Displaying Products"):
        url, image_url, body_content = entry  # Unpack the entry tuple
        print(f"URL: {url}\nImage URL: {image_url}\nBody Content: {body_content}\n")

if __name__ == "__main__":
    main()