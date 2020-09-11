from json import JSONDecoder
import pprint
from CONSTANTS import listing_key_list,listing_required_values, listing_required_values


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


def flatten_dict(myobj, separator=".."):
    # print(f"here for myobj: {myobj}")
    if isinstance(myobj, dict):
        return [k + separator + vv for k, v in myobj.items() if v is not None for vv in flatten_dict(v, separator)]
    elif isinstance(myobj, list):
        return [str(i) + separator + vv for i, v in enumerate(myobj) if v is not None for vv in flatten_dict(v, separator) if v]
    # elif isinstance(myobj, str):
    #     return [myobj]
    elif isinstance(myobj, (str, int, float)):
        return [str(myobj)]
    # elif isinstance(myobj, float):
    #     return [str(myobj)]
    else:
        print(f"Unknown object got: {type(myobj)}")

def get_data_from_dict(data_dict, separator=".."):
    new_dict = dict()
    for k, v in listing_required_values.items():
        key_list = v.split(separator)
        myitem = data_dict
        while key_list:
            key = key_list.pop(0)
            print(f"key: {key}")
            if key.isdigit():
                myitem = myitem[int(key)]
            elif (myitem := myitem.get(key)) is not None:
                pass
            else:
                print(f"Breaking. as {key} not in {myitem}")
                myitem = "NOT FOUND"
                break
                # raise Exception



        new_dict[k] = myitem if not isinstance(myitem, (list, dict)) else ""

    return new_dict

def get_listing_data(text):
    """
    Get the listing details from the listing page text
    :param text: Listing page text
    :return: Dictionary of listing details
    """
    data_dict =  {key: result.get(key) for result in extract_json_objects(text) for key in listing_key_list if
            key and result.get(key)}



    # priniting initial dictionary
    print("initial_dictionary", str(data_dict))

    flattenend_dict = flatten_dict(data_dict)

    # printing final dictionary
    print("final_dictionary", str(flattenend_dict))

    return data_dict

    # for result in extract_json_objects(text):
    #     for key in listing_key_list:
    #         if result.get(key):
    #
    #     if result.get('profiles'):
    #         pprint.pprint(result.get('profiles'))
    #     elif result:
    #         print("NEXT".center(25, "*"))
    #         pprint.pprint(result)


def using_api_key(api_key):
    pass
