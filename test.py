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

with open('listings.html', 'r') as f:
    demo_text = f.read()
# for result in extract_json_objects(demo_text.split("listingsMap", 1)[1]):
for result in extract_json_objects(demo_text):
    if result.get('profiles') :
        pprint.pprint(result.get('profiles'))
    elif result:
        print("NEXT".center(25, "*"))
        pprint.pprint(result)
"""
{'action': 'product', 'options': {'foo': 'bar'}}
{'action': 'review', 'options': {'spam': ['ham', 'vikings', 'eggs', 'spam']}}
"""