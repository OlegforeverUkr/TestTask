import requests
from bs4 import BeautifulSoup
import json

from requests import RequestException, HTTPError, Timeout


class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.data = {}


    def fetch_page(self):
        try:
            response = requests.get(self.url)
            return response.text
        except (RequestException, ConnectionError, HTTPError, Timeout) as e:
            raise RequestException(f"Bad request: {e}")


    def parse_page(self, html):
        soup = BeautifulSoup(html, "html.parser")

        # Find product title
        title = soup.find(id="itemTitle")
        if title:
            self.data["title"] = title.get_text().replace('Details about  \xa0', '')

        # Find product image
        image = soup.find(class_="ux-image-carousel-item image-treatment image")
        if image:
            img_tag = image.find("img")
            image_url = img_tag.get("src", '')
            self.data["image_url"] = image_url

        # Set product url
        self.data["product_url"] = self.url

        # Find product price
        price = soup.find(class_="x-price-primary")
        if price:
            self.data["price"] = price.get_text()
        else:
            self.data["price"] = "Not found!"

        # Find product seller
        seller = soup.find(class_="x-sellercard-atf__data-item-wrapper")
        if seller:
            self.data["seller"] = seller.get_text()


    def save_to_json(self, filename):
        with open(filename, "w") as json_file:
            json.dump(self.data, json_file, indent=4)


    def scrape(self):
        html = self.fetch_page()
        if html:
            self.parse_page(html)
            print(json.dumps(self.data, indent=4))


if __name__ == "__main__":
    url = "https://www.ebay.com/p/14038004460?iid=224861468077"
    scraper = EbayScraper(url)
    scraper.scrape()
    scraper.save_to_json('product_data.json')
