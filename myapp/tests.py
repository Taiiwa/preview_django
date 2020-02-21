from django.test import TestCase

# Create your tests here.
import json
user_info= '{"name" : "john", "gender" : "male", "age": 28}'
str = "{'a':1,'b':2}"
print(json.loads(user_info))