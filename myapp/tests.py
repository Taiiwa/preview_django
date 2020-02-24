from django.test import TestCase

# Create your tests here.
import uuid

ret = uuid.uuid4()
ret = str(ret)
print(ret)
print(type(ret))
# str = ('123.jpg')
# print(str[-4:])