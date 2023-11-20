import xml.etree.ElementTree as ET
import random
from tqdm import tqdm

def extract_sitemap_data(xml_file_path, search_terms, num_urls=15):
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
            image_caption = image.find('image:caption', namespaces).text.lower() if image.find('image:caption', namespaces) is not None else ""

            # Debugging print
            print(f"Checking image caption: {image_caption}")

            if all(term.lower() in image_caption for term in search_terms):
                image_title = image.find('image:title', namespaces).text.lower()
                products.append((loc, image_loc, image_title))
            else:
                # Debugging print
                print(f"Caption '{image_caption}' does not match all terms {search_terms}")

    return products

def main():
    xml_file_path = 'sitemap_products_1.xml'  # Replace with your XML file path
    search_terms = ['Fedora', 'Brown']  # Update search terms here
    random_entries = extract_sitemap_data(xml_file_path, search_terms)

    for entry in tqdm(random_entries, desc="Displaying Products"):
        print(f"Product URL: {entry[0]}\nImage URL: {entry[1]}\nTitle: {entry[2]}\n")

if __name__ == "__main__":
    main()
