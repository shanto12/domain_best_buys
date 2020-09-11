from time import sleep
import requests
import pprint
from bs4 import BeautifulSoup
import pandas
import re
from find_working_proxy import find_proxies
from extract_data import get_house_data, get_listing_data, get_data_from_dict
from functions import blockPrint, enablePrint, decorated_print
print = decorated_print

PROXIES = None
# PROXIES = "TEST"  # To test without proxies in the http_call
BASE_URL = "https://www.domain.com.au"
LIMIT=5
# EXCLUDE_UNDER_OFFER = 1
non_conventional_url ="https://www.domain.com.au/project/4194/havana-dee-why-nsw/"



class SearchListings:
    def __init__(self, property_type, suburb_post):
        self.property_type = property_type
        self.suburb_post = suburb_post

    def http_call(self, url, proxies=None, **kwargs):
        global PROXIES

        # proxies = None if PROXIES == "TEST" else proxies
        # for i in range(3):
        #     try:
        #         r = requests.get(url, params=kwargs, proxies=proxies)
        #     except Exception as e:
        #         print(e)
        #         print(f"{i}: Trying to get a different proxy")
        #         proxies = find_proxies()
        #     else:
        #         print(f"Executed URL: {r.url}. Status: {r.ok}. Status Code: {r.status_code}. Reason: {r.reason}")
        #         return BeautifulSoup(r.content, 'lxml')
        if PROXIES == "TEST":
            try:
                r = requests.get(url, params=kwargs, proxies=None)
            except Exception as e:
                print(e)
            else:
                print(f"Executed URL: {r.url}. Status: {r.ok}. Status Code: {r.status_code}. Reason: {r.reason}")
                return BeautifulSoup(r.content, 'lxml')
        else:
            print(f"There are {len(proxies.values())} prixies now")
            while 1:
                for i, proxy in enumerate(proxies.values()):
                    try:
                        print(f"{i}: Making call with proxy: {proxy}")
                        r = requests.get(url, params=kwargs, proxies=proxy)
                    except Exception as e:
                        print(e)
                        print(f"exception while using proxy: {proxy}")
                        # print(f"{i}: Trying to get a different proxy")
                        # proxies = find_proxies()
                    else:
                        print(f"Executed URL: {r.url}. Status: {r.ok}. Status Code: {r.status_code}. Reason: {r.reason}")
                        return BeautifulSoup(r.content, 'lxml')
                seconds = 10
                print(f"Sleeping {seconds} seconds")
                sleep(seconds)

    def get_listings_from_html(self, url, parent_attr_dict, **kwargs):
        soup = self.http_call(url=url, proxies=PROXIES, **kwargs)
        if soup and soup.find_all('ul', parent_attr_dict) and soup.find_all('ul', parent_attr_dict)[0]:
            listings_url_set = {x.get('href') for x in soup.find_all('ul', parent_attr_dict)[0].find_all('a')}
        else:
            listings_url_set = set()
        return listings_url_set

    def get_properties_from_html(self, url, parent_attr_dict=None, **kwargs):
        soup = self.http_call(url=url, proxies=PROXIES, **kwargs)
        soup_html = str(soup)
        data_dict = get_listing_data(soup_html)
        # pprint.pprint(data_dict)
        data_dict = get_data_from_dict(data_dict)
        print("2".center(50, "="))
        for key in ["features", "description", "otherListingsIds_list"]:
            data_dict[key] = ", ".join(map(str, data_dict[key]))
        del data_dict["location_profiles_list"]
        pprint.pprint(data_dict)

        return data_dict



    def get_listing_page_urls(self):
        parent_attr_dict = {"data-testid": "results"}

        page = 1
        listing_url_set = set()

        url = f"{BASE_URL}/{self.property_type}/{self.suburb_post}/"
        print(f"Getting urls from page: {url}")
        # while (not LIMIT or page<=LIMIT) and (url_set:=self.get_listings_from_html(url=url, parent_attr_dict=parent_attr_dict, excludeunderoffer=EXCLUDE_UNDER_OFFER, page=page)):
        while (not LIMIT or page <= LIMIT) and (
        url_set := self.get_listings_from_html(url=url, parent_attr_dict=parent_attr_dict,page=page)):
            listing_url_set.update(url_set)
            page += 1

        return listing_url_set

    def df_to_csv(self, df, csv_name):
        df.to_csv(csv_name, index=False)
        print("created csv")

    def get_data_from_listings(self, url_list):
        # parent_attr_dict = {"data-testid": "page"}
        data_dict_list = []
        for i, url in enumerate(url_list[:LIMIT]):
            print(f"{i}: {url}")
            data_dict_list.append(self.get_properties_from_html(url=url))

        return pandas.DataFrame(data_dict_list)


if __name__ == "__main__":
    print("SCRIPT STARTED".center(50, "="))
    # blockPrint()
    PROXIES = find_proxies()
    # enablePrint()
    print(f"Found {len(PROXIES)} proxies")
    if PROXIES:
        # PROXIES = list(PROXIES.values())
        pprint.pprint(PROXIES)
        print("PROXY PART DONE".center(50, "="))
        # search_listings_obj = SearchListings(property_type="sale", suburb_post="dee-why-nsw-2099")
        # search_listings_obj = SearchListings(property_type="rent", suburb_post="dee-why-nsw-2099")
        search_listings_obj = SearchListings(property_type="sold-listings", suburb_post="dee-why-nsw-2099")


        listing_url_set = search_listings_obj.get_listing_page_urls()
        pprint.pprint(listing_url_set)

        # listing_df = search_listings_obj.get_data_from_listings({"https://www.domain.com.au/239-17-howard-avenue-dee-why-nsw-2099-2016430909"})
        listing_df = search_listings_obj.get_data_from_listings(list(listing_url_set))
        search_listings_obj.df_to_csv(listing_df, "listings2.csv")


    print("SCRIPT FINISHED".center(50, "="))