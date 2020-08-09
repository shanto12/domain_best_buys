import requests
import pprint
from bs4 import BeautifulSoup

BASE_URL = "https://www.domain.com.au"
LIMIT=None
EXCLUDE_UNDER_OFFER = 1
PROXIES = {"https": "https://217.69.9.154:8080"}
non_conventional_url ="https://www.domain.com.au/project/4194/havana-dee-why-nsw/"


class SearchListings:
    def __init__(self, property_type, suburb_post):
        self.property_type = property_type
        self.suburb_post = suburb_post

    def http_call(self, url, proxies=None, **kwargs):
        r = requests.get(url, params=kwargs, proxies=proxies)
        print(f"Executed URL: {r.url}. Status: {r.ok}. Status Code: {r.status_code}")
        return BeautifulSoup(r.content, 'lxml')




    def get_listings_from_html(self, url, parent_attr_dict, **kwargs):
        soup = self.http_call(url=url, proxies=PROXIES, **kwargs)
        if soup.find_all('ul', parent_attr_dict) and soup.find_all('ul', parent_attr_dict)[0]:
            listings_url_set = {x.get('href') for x in soup.find_all('ul', parent_attr_dict)[0].find_all('a')}
        else:
            listings_url_set = set()
        return listings_url_set

    def get_properties_from_html(self, url, parent_attr_dict=None, **kwargs):
        soup = self.http_call(url=url, proxies=PROXIES, **kwargs)
        page_el = soup.find_all('div', class_="listing-details__root")
        for child_el in page_el[0].findChildren():
            for attribute in ["attrs", "id", "text", "value", "name"]:
                print(f"{attribute}: {getattr(child_el, attribute)}")

            print("\n")

        # listings_url_set = {x.get('href') for x in soup.find_all('ul', parent_attr_dict)[0].find_all('a')}
        print('')
        # return listings_url_set


    def get_listing_page_urls(self):
        parent_attr_dict = {"data-testid": "results"}

        page = 1
        listing_url_set = set()

        url = f"{BASE_URL}/{self.property_type}/{self.suburb_post}/"
        print(f"Getting urls from page: {url}")
        while (not LIMIT or page<=LIMIT) and (url_set:=self.get_listings_from_html(url=url, parent_attr_dict=parent_attr_dict, excludeunderoffer=EXCLUDE_UNDER_OFFER, page=page)):
            listing_url_set.update(url_set)
            page += 1

        return listing_url_set

    def get_data_from_listings(self, url_set):
        # parent_attr_dict = {"data-testid": "page"}
        for url in url_set:
            # soup = self.http_call(url, proxies=PROXIES)
            self.get_properties_from_html(url=url)

# def proxy_test(proxies=None):
#
#     url = "https://www.myip.com/"
#
#     r = requests.get(url, proxies=proxies)
#     # r = requests.get(url)
#
#     soup = BeautifulSoup(r.content, features="lxml")
#     els = soup.find_all(id="ip")
#     print(f'IP: {els[0].text}')




# for i in range(2):
#     proxy_test()
search_listings_obj = SearchListings(property_type="sale", suburb_post="dee-why-nsw-2099")
# search_listings_obj.get_data_from_listings({"https://www.domain.com.au/project/4194/havana-dee-why-nsw/"})
listing_url_set = search_listings_obj.get_listing_page_urls()
# pprint.pprint(listing_url_set)
