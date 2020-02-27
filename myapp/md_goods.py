from django.shortcuts import render, redirect
# 导包
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# 导入类视图
from django.views import View

from myapp.models import User
import json
from django.core.serializers import serialize
from rest_framework.response import Response
from rest_framework.views import APIView
# 导入加密库
import hashlib
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

import hmac

# 导入上传文件夹配置
from mydjango.settings import UPLOAD_ROOT
import os

# 导入原生sql模块
from django.db import connection

import jwt
import urllib
import base64

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

from .models import *
from .myser import *


# 获取分类信息
"""
增删改查操作，可以通过调用接口的不同方式来执行，get来获取，post来添加，put来修改，delete来删除，通过类属性获取数据，从而节省接口和代码，时间关系先不回头改了
"""
class GetCate(APIView):
    def get(self, request):
        # 从数据库获取所有分类信息
        cate = Category.objects.all()
        ser = CategorySer(cate, many=True)
        res = {}
        res['code'] = 200
        res['data'] = ser.data
        return Response(res)

# 修改分类
class ResetCate(APIView):
    def get(self,request):
        # 获取参数：
        cid = request.GET.get('cid')
        cate = request.GET.get('cate')
        print(cid)
        print(cate)
        # 修改数据库中的数据
        res = {}
        try:
            category = Category.objects.filter(id=int(cid)).first()
            print(category)
            print(category.cate)
            category.cate = cate
            category.save()
            res['code'] = 200
            return Response(res)
        except:
            res['code'] = 405
            return Response(res)


# 添加分类
class AddCate(APIView):
    def get(self,request):
        new_cate = request.GET.get('new_cate')
        # 更新数据库
        new_cate = Category(cate=new_cate)
        new_cate.save()
        return Response({'code':200})

# 删除分类
class DeleteCate(APIView):
    def get(self,request):
        # 获取数据
        id = request.GET.get('id')
        cate = Category.objects.filter(id=id).first()
        cate.delete()
        res = {}
        res['code'] = 200

        return Response(res)


# 接收图片接口
# 上传文件
class UploadGoodsPicture(APIView):
    def post(self, request):
        # 定义相应对象
        res = {}
        # 后端获取文件名，以uuid重命名，并保存到本地
        myFile = request.FILES.get('file')
        file_name = str(uuid.uuid4()) + myFile.name[-4:]
        f = open(os.path.join(UPLOAD_ROOT, 'goods/image_packs/', file_name), 'wb')
        for chunk in myFile.chunks():
            f.write(chunk)
        # 关闭文件流
        f.close()

        #  5，后端尝试获取localStorage中的临时图片，如果获取到了，则删除

        temp_img = request.POST.get('temp_goods_picture')

        if temp_img:
            try:
                os.remove('./static/upload/goods/image_packs/' + temp_img)
            except:
                pass

        # 返回新图片名
        res['data'] = file_name
        return Response(res)

# 接收视频接口
# 上传文件
class UploadGoodsVideo(APIView):
    def post(self, request):
        # 定义相应对象
        res = {}
        # 后端获取文件名，以uuid重命名，并保存到本地
        myFile = request.FILES.get('file')
        file_name = str(uuid.uuid4()) + myFile.name[-4:]
        f = open(os.path.join(UPLOAD_ROOT, 'goods/media/', file_name), 'wb')
        for chunk in myFile.chunks():
            f.write(chunk)
        # 关闭文件流
        f.close()

        #  5，后端尝试获取localStorage中的临时图片，如果获取到了，则删除

        temp_video = request.POST.get('temp_goods_media')

        if temp_video:
            try:
                os.remove('./static/upload/goods/media/' + temp_video)
            except:
                pass

        # 返回新视频名
        res['data'] = file_name
        return Response(res)


# 商品入库接口
class AddGoods(APIView):
    def get(self, request):
        name = request.GET.get('name')
        desc = request.GET.get('desc')
        param = request.GET.get('param')
        video = request.GET.get('video')
        img = request.GET.get('img')
        price = request.GET.get('price')
        cid = request.GET.get('cate')

        print(name)
        print(cid)
        print(price)
        print(desc)
        print(param)
        print(video)
        print(img)
        res = {}
        # 排重
        goods = Goods.objects.filter(name=name).first()
        if goods:
            res['code'] = 405
            res['message'] = '商品已经存在'
            return Response(res)

        # 进行入库
        goods = Goods(name=name, desc=desc, img=img, video=video, param=param, cid=cid, price=price)
        goods.save()

        res['code'] = 200
        res['message'] = '商品添加成功'

        return Response(res)


# 商品列表页
class GoodsList(APIView):
    def get(self, request):
        # 获取用户id
        uid = request.GET.get('uid')

        # 读取数据库
        user = User.objects.filter(id=int(uid)).first()

        # 进行序列化操作
        user_ser = UserSer(user)

        # 进行返回
        return Response(user_ser.data)


# 定义地址和端口
host = '127.0.0.1'
port = 6379

# 建立redis链接
r = redis.Redis(host=host, port=port)
