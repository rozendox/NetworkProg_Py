import json

# print
electron = 1.60218e-19
print(json.dumps(electron))

# intro a list
my_list = [1, 2.34, True, "False", None, ['a', 0]]
print(json.dumps(my_list))


# check the dictionary
my_dict = {'me': "Python",
           'pi': 3.141592653589793,
           'data': (1,2,3,4),
           'set': None,
           'list_1': [1.2, 3, True] }

print(json.dumps(my_dict))

"""
JSON cannot distinguish between lists and tuples, 
both of these are converted into JSON arrays.

JSON não consegue destiguir entre listas ou tuplas.
Ambos são convertidos em arrays "jeisonnn" 
"""


