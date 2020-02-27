from django.db import models


#基类
class Base(models.Model):

    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True

# 商品表
class Goods(Base):
    # 商品名
    name = models.CharField(max_length=200)
    # 商品秒数
    desc = models.CharField(max_length=500)
    # 商品头图
    img = models.CharField(max_length=200)
    # 商品规格
    param = models.CharField(max_length=500)
    # 商品类别      使用逻辑外键而不是物理外键
    cid = models.IntegerField()
    # 演示视频
    video = models.CharField(max_length=200)
    # 关注
    follow = models.IntegerField(default=0, null=True)
    # 价格
    price = models.IntegerField()

    class Meta:
        db_table = 'goods'

# 商品分类表
class Category(Base):
    cate = models.CharField(max_length=200)

    class Meta:
        db_table = 'category'


#用户表
class User(Base):

    #用户名
    username = models.CharField(max_length=200)
    #密码
    password = models.CharField(max_length=200)
    #头像
    img = models.CharField(max_length=200)
    #类别 0普通用户 1代表管理员 2代表商家
    type = models.IntegerField()

    #声明表名
    class Meta:
        db_table = "user"

