"""
pra cada tipo pythonico a gente tem um tipo jeison

python data   |  Json element
dict             object
list or tuple    array
int or float     number
True/False       true/false
None             null

isso parece bem consistente porém...
não podemos dar dump num conteúdo de um objeto:

class Who:
    def __init__(self, name, age):
        self.name = name
        self.age = age


some_man = Who('John Doe', 42)
print(json.dumps(some_man))

output:
TypeError: Object of type 'Class' is not JSON serializable

"""

import json


class Who:
    def __init__(self, name, age):
        self.name = name
        self.age = age


def encode_who(w):
    if isinstance(w, Who):
        return w.__dict__
    else:
        raise TypeError(w.__class__.__name__ + ' is not JSON serializable')


some_man = Who('John Doe', 42)
print(json.dumps(some_man, default=encode_who))