from django.shortcuts import render, redirect
# 导包
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# 导入类视图
from django.views import View

# from myapp.models import User
import json
from django.core.serializers import serialize
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
# 导入加密库
import hashlib
# 导入解密库
# from django.contrib.auth.hashers import check_password
# 导入图片库
# 绘画库
from PIL import ImageDraw
# 字体库
from PIL import ImageFont
# 图片库
from PIL import Image
# 随机库
import random
# 文件流
import io

import requests

# 导入上传文件夹配置
from mydjango.settings import UPLOAD_ROOT
import os

# 导入原生sql模块
from django.db import connection

import jwt
import urllib
import base64
import hmac

# 导入redis数据库
import redis

# 导入时间模块
import time

# 导入公共目录变量
from mydjango.settings import BASE_DIR

# 导包
from django.db.models import Q, F

# 导入dwebsocket的库
from dwebsocket.decorators import accept_websocket
import uuid

# 导入数据库
from .models import *

# 导入验证码包
from utils.captcha.captcha import captcha

#   七牛云相关
from qiniu_key.config import AK, SK
from qiniu import Auth


# 七牛云秘钥接口
class Qiniu(APIView):
    def get(self, request):
        # 声明秘钥对象
        q = Auth(AK, SK)

        # 生成令牌
        token = q.upload_token('huabeimissty')

        return Response({
            'up_token': token
        })


# 修改密码
class PasswordChange(APIView):
    def post(self,request):
        # 接收数据
        uid = request.POST.get('uid')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')

        # 构建返回对象
        res = {}

        # 比对原密码
        user = User.objects.get(id=uid)
        if make_password(old_password) == user.password:
            user.password = make_password(new_password)
            user.save()
            res['code'] = 200
            return Response(res)

        res['code'] = 405
        return Response(res)

# 修改头像，入库
class ConSubmit(APIView):
    def get(self, request):
        # 获取传入的uid和头像
        uid = request.GET.get('uid')
        img = request.GET.get('img')

        # 入库
        user = User.objects.get(id=uid)
        user.img = img
        user.save()

        res = {}
        res['code'] = 200
        res['message'] = '上传成功'

        return Response(res)


# 退出修改页面，删除缓存图片
class DeleteTempImg(APIView):
    def get(self, request):
        # 获取目标图片：
        temp_img = request.GET.get('temp_img')
        #删除
        if temp_img:
            try:
                os.remove('./static/upload/' + temp_img)
            except:
                pass
        res = {}
        res['code'] = 200

        return Response(res)


# 上传文件
class UploadFile(APIView):
    def post(self, request):
        # 定义相应对象
        res = {}
        # user = User.objects.filter(username=username).first()
        # # 获取图片名，清理当前本地储存或七牛云储存的图片
        # pre_img = user.img
        # if pre_img:
        #     pre_img_name = pre_img.split('/')[-1]
        #     try:
        #         os.remove('./static/upload/' + pre_img_name)
        #     except:
        #         pass
        # 【【【4，后端获取文件名，以uuid重命名，并保存到本地】】】
        myFile = request.FILES.get('file')
        file_name = str(uuid.uuid4()) + myFile.name[-4:]
        f = open(os.path.join(UPLOAD_ROOT, '', file_name), 'wb')
        for chunk in myFile.chunks():
            f.write(chunk)
        # 关闭文件流
        f.close()

        #  【【【5，后端尝试获取localStorage中的临时头像，如果获取到了，则删除】】】

        temp_img = request.POST.get('temp_img')

        if temp_img:
            try:
                os.remove('./static/upload/' + temp_img)
            except:
                pass

        # 返回新头像名
        res['data'] = file_name

        # # 需要填写你的 Access Key 和 Secret Key
        # access_key = settings.AK
        # secret_key = settings.SK
        # # 构建鉴权对象
        # q = Auth(access_key, secret_key)
        # # 要上传的空间
        # bucket_name = settings.BUCKET_NAME
        # # 上传后保存的文件名
        # key = None  # 不指定文件名
        # # 生成上传 Token，可以指定过期时间等
        # token = q.upload_token(bucket_name, key, 3600)
        # # 要上传文件的本地路径  #提交数据 到七牛云
        # ret, info = put_data(token, key, myFile.read())  # info是响应的详情   ret是响应的一部分 返回hash和key
        # pic1 = ""
        # if info.status_code == 200:
        #     # 上传七牛云成功
        #     pic1 = settings.QINIU_HOST + "/" + ret.get("key")
        # request.data['img'] = pic1
        #
        # # 如果用七牛云，则是在数据库中存储七牛云中的图片名称：
        # print(pic1)

        return Response(res)


# 上传视频音频
class MediaFile(APIView):
    def post(self, request):
        print('调用接口')
        # 定义相应对象
        res = {}
        # 接收文件
        myFile = request.FILES.get('file')
        # 建立文件流对象
        print('-' * 100)
        file_name = myFile.name
        print('*' * 100)
        print(file_name)
        f = open(os.path.join(UPLOAD_ROOT, 'media/', file_name), 'wb')
        for chunk in myFile.chunks():
            f.write(chunk)
        # 关闭文件流
        f.close()

        # 生成地址
        src = 'http://127.0.0.1:8000/static/upload/media/' + file_name
        res['data'] = src

        return Response(res)


# MD5加密方法：
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
    return md5_server


# MD5验证方法
# def check_password(mypass):
#     md5 = hashlib.md5()


# 钉钉登录回调视图
def ding_back(request):
    # 获取code
    code = request.GET.get("code")

    t = time.time()
    # 时间戳
    timestamp = str((int(round(t * 1000))))
    appSecret = 'ly-AzMKMmCKQP3geaILT_An32kEfKO3HeOtApy5CgKwjytevVZC0WYsT2gxMB160'
    # 构造签名
    signature = base64.b64encode(
        hmac.new(appSecret.encode('utf-8'), timestamp.encode('utf-8'), digestmod=hashlib.sha256).digest())
    # 请求接口，换取钉钉用户名
    payload = {'tmp_auth_code': code}
    headers = {'Content-Type': 'application/json'}
    res = requests.post('https://oapi.dingtalk.com/sns/getuserinfo_bycode?signature=' + urllib.parse.quote(
        signature.decode("utf-8")) + "&timestamp=" + timestamp + "&accessKey=dingoaukgkwqknzjvamdqh",
                        data=json.dumps(payload), headers=headers)

    res_dict = json.loads(res.text)

    # 获取相关登录信息，拼接用户名
    # 业务逻辑：一般平台的账号（用户名）和昵称是分离的。一般账号是英文数字下划线组成，百度支持中文账号，但不可修改。昵称支持中文，可以修改或重复。所以应该有账号（唯一字段）和昵称（不唯一字段）两个字段。这里为实验项目，暂不考虑重名，将昵称作为账号存入。
    # uid = res_dict.get('user_info).get('unionid')

    username = res_dict.get('user_info').get('nick')
    print(res_dict)
    print(username)
    # 检查该用户名是否登陆过，如果没有，创建新用户
    user = User.objects.filter(username=username).first()
    if not user:
        user_ding = User(username=username, password="", img='', type=0)
        user_ding.save()
    res = {}
    res['code'] = 200

    res['username'] = username

    id = User.objects.filter(username=username).first().id

    res['uid'] = id
    return HttpResponseRedirect('http://localhost:8080/dingding?username=%s&uid=%s/' % (username, id))


    # return JsonResponse(res_dict)


# 新浪微博回调视图
def weibo_back(request):
    # 获取code
    code = request.GET.get('code')

    # 换取网址
    access_token_url = "https://api.weibo.com/oauth2/access_token"

    # 发送请求进行换取
    re_dict = requests.post(
        access_token_url,
        data={
            "client_id": '2636039333',
            "client_secret": "4e2fbdb39432c31dc5c2f90be3afa5ce",
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://127.0.0.1:8000/md_admin/weibo"
        }
    )

    # 获取相关登录信息，拼接用户名
    uid = json.loads(re_dict.text).get('uid')
    username = '游客' + uid
    # 检查该用户名是否登陆过，如果没有，创建新用户
    user = User.objects.filter(username=username).first()
    if not user:
        user_weibo = User(username=user, password=uid, img='', type=0)
        user_weibo.save()
    res = {}
    res['code'] = 200

    res['username'] = username

    id = User.objects.filter(username=username).first().id

    res['uid'] = id
    return HttpResponseRedirect('http://localhost:8080/weibo?username=%s/' % uid)


# 生成验证码：
def make_code(request):
    name, text, img = captcha.generate_captcha()
    # 写入session
    # request.session['code'] = text        # 可以成功设置
    # 将验证码存入到cache，设置生命周期
    cache.set('code', text, 360)
    return HttpResponse(img)


# 注册接口
class Reg(APIView):
    def get(self, request):
        # 定义响应数据
        res = {}
        # 接收交互数据
        username = request.GET.get('username', '未收到用户名')
        password = request.GET.get('password', '未收到密码')
        password = make_password(password)
        code = request.GET.get('code', '未收到验证码').upper()
        user = User.objects.filter(username=username)
        # 验证用户名是否重复
        if user:
            res['code'] = 405
            res['message'] = '用户名已存在'
            return Response(res)
        # 验证验证码是否正确
        if code.upper() != cache.get('code'):
            # if code.upper() != request.session.get('code'):       #读取不到
            print(request.session.get('code'))
            res['code'] = 405
            res['message'] = '验证码错误'
            return Response(res)
        res = {}
        res['code'] = 200
        res['message'] = '注册成功'
        user_data = User(username=username, password=password, img='', type=0)
        user_data.save()
        return Response(res)


# 登录接口
class Login(APIView):
    def get(self, request):
        res = {}
        username = request.GET.get('username')
        password = request.GET.get('password')

        # 验证码

        # 检查用户名和密码
        user = User.objects.filter(username=username).first()
        if user:

            if make_password(password) == user.password:
                res['code'] = 200
                res['message'] = '登录成功'
                res['username'] = user.username
                res['uid'] = user.id
                res['type'] = user.type
                # 头像
                res['img'] = user.img
            else:
                res['code'] = 405
                res['message'] = '用户名或密码错误'
        else:
            res['code'] = 405
            res['message'] = '用户名或密码错误'
        return Response(res)


# 微博登录跳转页面
class WeiBo(APIView):
    def get(self, request):
        uid = request.GET.get('uid')
        username = '游客' + uid
        print(username)
        user = User.objects.filter(username=username).first()
        res = {}
        if user:
            res['code'] = 200
            res['username'] = user.username
            res['uid'] = user.id
            res['message'] = '登录成功'
        else:
            res['code'] = 400
            res['message'] = '出现未知错误'
        return Response(res)
