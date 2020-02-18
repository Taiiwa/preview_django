from django.db import models


#基类
class Base(models.Model):

    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


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