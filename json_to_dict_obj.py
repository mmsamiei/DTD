import json
import demjson

class User:
    def __init__(self, **entries):
        self.state = "start"
        if entries:
            self.__dict__.update(entries)

with open('data.json', 'r') as fp:
	temp_dict = json.load(fp)
print(temp_dict)
print(temp_dict["73675932"])
s = User(**temp_dict["73675932"])
print(s)
print(s.state)

user_dict = {}
for k, v in temp_dict.items():
    user_dict[k] = User(**v)
    print(k, v)

print(user_dict)