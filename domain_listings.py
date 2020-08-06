import requests
import pprint
from bs4 import BeautifulSoup

BASE_URL = "https://www.domain.com.au"
LIMIT=1
EXCLUDE_UNDER_OFFER = 1

class SearchListings:
    def __init__(self, property_type, suburb_post):
        self.property_type = property_type
        self.suburb_post = suburb_post

    def http_call(self, url, **kwargs):
        r = requests.get(url, params=kwargs)
        return BeautifulSoup(r.content, 'html.parser')

    def get_listings(self, url, parent_attr_dict, **kwargs):
        soup = self.http_call(url=url, **kwargs)
        listings_url_set = {x.get('href') for x in soup.find_all('ul', parent_attr_dict)[0].find_all('a')}

        # pprint.pprint(listings_url_set)

        return listings_url_set


    def get_listing_page_urls(self):
        parent_attr_dict = {"data-testid": "results"}
        page = 1
        listing_url_set = set()

        url = f"{BASE_URL}/{self.property_type}/{self.suburb_post}/"
        while page<=LIMIT and (url_set:=self.get_listings(url=url, parent_attr_dict=parent_attr_dict, excludeunderoffer=EXCLUDE_UNDER_OFFER, page=page)):
            listing_url_set.update(url_set)
            page += 1

        return listing_url_set

    def get_data_from_listings(self, url_set):
        for url in url_set:
            soup = self.http_call(url)
            print(soup)





search_listings_obj = SearchListings(property_type="sale", suburb_post="dee-why-nsw-2099")
search_listings_obj.get_data_from_listings({"https://www.domain.com.au/10-10-avon-road-dee-why-nsw-2099-2016418017"})
# listing_url_set = search_listings_obj.get_listing_page_urls()
# pprint.pprint(listing_url_set)
