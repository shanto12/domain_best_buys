import os


def decorated_print(obj):
    print(f"{os.getpid()}: {obj}")

# print = decorated_print
decorated_print("hello")

# json_path = "listing.json"
#
# def read_json(json_path):
#     with open(json_path, 'r') as f:
#         return json.loads(f.read())
#
#
# def get_values_from_dict():
#     pass
#
#
# def shanto_flatten_dict(myobj):
#     # print(f"here for myobj: {myobj}")
#     if isinstance(myobj, dict):
#         return [k + ".." + vv for k, v in myobj.items() for vv in shanto_flatten_dict(v)]
#     elif isinstance(myobj, list):
#         return [str(i) + ".." + vv for i, v in enumerate(myobj) for vv in shanto_flatten_dict(v)]
#     # elif isinstance(myobj, str):
#     #     return [myobj]
#     elif isinstance(myobj, (str, int, float)):
#         return [str(myobj)]
#     # elif isinstance(myobj, float):
#     #     return [str(myobj)]
#     else:
#         print(f"Unknown object got: {type(myobj)}")
#
# mydict = read_json(json_path)
#
# flattened_dict = shanto_flatten_dict(mydict)
#
# pprint.pprint(flattened_dict)

# from json import JSONDecoder
# import pprint
#
# def extract_json_objects(text, decoder=JSONDecoder()):
#     """Find JSON objects in text, and yield the decoded JSON data
#
#     Does not attempt to look for JSON arrays, text, or other JSON types outside
#     of a parent JSON object.
#
#     """
#     pos = 0
#     while True:
#         match = text.find('{', pos)
#         if match == -1:
#             break
#         try:
#             result, index = decoder.raw_decode(text[match:])
#             yield result
#             pos = match + index
#         except ValueError:
#             pos = match + 1
#
# with open('listings.html', 'r') as f:
#     demo_text = f.read()
# # for result in extract_json_objects(demo_text.split("listingsMap", 1)[1]):
# for result in extract_json_objects(demo_text):
#     if result.get('profiles') :
#         pprint.pprint(result.get('profiles'))
#     elif result:
#         print("NEXT".center(25, "*"))
#         pprint.pprint(result)
# """
# {'action': 'product', 'options': {'foo': 'bar'}}
# {'action': 'review', 'options': {'spam': ['ham', 'vikings', 'eggs', 'spam']}}
# """