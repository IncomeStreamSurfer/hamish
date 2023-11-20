import xml.etree.ElementTree as ET
import random
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
 
def extract_product_info(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
 
        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else 'No title available'
 
        description_tag = soup.find('div', {'class': 'product__description rte quick-add-hidden'})
        description = description_tag.get_text(strip=True) if description_tag else 'No description available'
 
        price_tag = soup.find('span', {'class': 'price-item--regular'})
        price = price_tag.get_text(strip=True) if price_tag else 'No price available'
 
        return title, description, price
    except Exception as e:
        return 'Failed to retrieve product info'
 
def extract_sitemap_data(xml_file_path, search_terms, num_urls=30):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()
 
    namespaces = {
        'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
        'image': 'http://www.google.com/schemas/sitemap-image/1.1'
    }
 
    products = []
    for url in tqdm(root.findall('ns:url', namespaces), desc="Processing URLs"):
        if len(products) >= num_urls:
            break  # Stop processing once 20 valid URLs are found
 
        loc = url.find('ns:loc', namespaces).text
        image = url.find('image:image', namespaces)
        if image is not None:
            image_loc = image.find('image:loc', namespaces).text
            image_title = image.find('image:title', namespaces).text.lower()
            if any(term.lower() in image_title for term in search_terms):
                title, description, price = extract_product_info(loc)
                products.append((loc, image_loc, title, description, price))
 
    return products
 
def main():
    xml_file_path = 'sitemap_products_1.xml'  # Replace with your XML file path
    search_terms = ['Fedora']  # Add your search terms here
    random_entries = extract_sitemap_data(xml_file_path, search_terms)
 
    for entry in tqdm(random_entries, desc="Displaying Products"):
        print(f"URL: {entry[0]}\nImage URL: {entry[1]}\nTitle: {entry[2]}\nDescription: {entry[3]}\nPrice: {entry[4]}\n")
 
if __name__ == "__main__":
    main()