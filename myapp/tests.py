from django.test import TestCase

# Create your tests here.
import hashlib

def make_password(mypass):
    # 重名方法自动重写
    # 生成MD5对象
    md5 = hashlib.md5()
    # 定义加密对象
    sign_str = mypass
    # 转码
    sign_utf8 = str(sign_str).encode(encoding='utf-8')
    # 加密操作
    md5.update(sign_utf8)
    # 生成密文
    md5_server = md5.hexdigest()
    print(md5_server)


if __name__ == '__main__':

    make_password("12345")