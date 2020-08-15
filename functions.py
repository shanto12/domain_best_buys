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

def using_api_key(api_key):
    pass
