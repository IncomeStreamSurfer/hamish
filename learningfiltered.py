import xml.etree.ElementTree as ET
import random
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

def extract_product_info(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        title_tag = soup.find('h1')
        title = title_tag.get_text(strip=True) if title_tag else 'No title available'

        # Scraping the Twitter description meta tag
        twitter_description_tag = soup.find('meta', {'name': 'twitter:description'})
        twitter_description = twitter_description_tag['content'] if twitter_description_tag else 'No Twitter description available'

        # Other scraping details can be included here as per your need

        return title, twitter_description
    except Exception as e:
        return 'Failed to retrieve product info', 'No Twitter description available'

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

        if image is not None:
            image_loc = image.find('image:loc', namespaces).text
            image_title = image.find('image:title', namespaces).text.lower()
            
            # Check if all search terms are in loc or image_title
            if all(term.lower() in loc.lower() for term in search_terms) or \
               all(term.lower() in image_title for term in search_terms):
                product_info = extract_product_info(loc)
                products.append((loc, image_loc, *product_info))

    return products

def main():
    xml_file_path = 'sitemap_products_14.xml'  # Replace with your XML file path
    search_terms = ['bluetooth', 'headset']  # Replace with your search terms
    random_entries = extract_sitemap_data(xml_file_path, search_terms)

    for entry in tqdm(random_entries, desc="Displaying Products"):
        print(f"URL: {entry[0]}\nImage URL: {entry[1]}\nTitle: {entry[2]}\nTwitter Description: {entry[3]}\n")

if __name__ == "__main__":
    main()
