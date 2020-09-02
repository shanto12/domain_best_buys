from json import JSONDecoder
import pprint


def extract_json_objects(text, decoder=JSONDecoder()):
    """Find JSON objects in text, and yield the decoded JSON data

    Does not attempt to look for JSON arrays, text, or other JSON types outside
    of a parent JSON object.

    """
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield result
            pos = match + index
        except ValueError:
            pos = match + 1

def get_house_data(text):
    import json



    start = 'listingsMap'
    end = 'totalListings'

    if start in text and end in text:
        first_index = text.index(start)
        second_index = text.index(end)
        our_text = text[first_index:second_index]
        if len(our_text) > 50:
            modified_text = '{"' + our_text[:-2] + '}'
            house_listing_dict = json.loads(modified_text)['listingsMap']
            return house_listing_dict
            # suburb_insight.extend([x['listingModel'] for x in house_listing_dict.values()])
        else:
            print("no")


def get_listing_data(text):
    """
    Get the listing details from the listing page text
    :param text: Listing page text
    :return: Dictionary of listing details
    """

    for result in extract_json_objects(text):
        if result.get('profiles'):
            pprint.pprint(result.get('profiles'))
        elif result:
            print("NEXT".center(25, "*"))
            pprint.pprint(result)


def using_api_key(api_key):
    pass
