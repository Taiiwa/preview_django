from django.test import TestCase

# Create your tests here.
from utils.captcha.captcha import captcha
name, text, img = captcha.generate_captcha()
print(name)
print(text)
print(img)
print(type(img))