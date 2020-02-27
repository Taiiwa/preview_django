#导包
from rest_framework import serializers
#导入数据库类
from .models import *

# 声明序列化对象类
class UserSer(serializers.ModelSerializer):

    # 声明字段
    class Meta:
        model = User
        fields = '__all__'


class GoodsSer(serializers.ModelSerializer):

    class Meta:
        model = Goods
        fields = '__all__'

class CategorySer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'
