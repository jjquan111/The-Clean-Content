from django.db import models


class detects(models.Model):
    detectcontent = models.CharField(max_length=2320)
    detectresult = models.CharField(max_length=2320)
    def __str__(self):
        return self.detectcontent

    class Meta:
        verbose_name = "敏感信息过滤管理"
        verbose_name_plural = verbose_name
        db_table = 'detectinfo'

# Create your models here.
class UserInfo(models.Model):
    """
    学生信息表
    """
    username = models.CharField(max_length=32,unique=True,verbose_name="用户名")
    password = models.CharField(max_length=64,verbose_name="密码")
    email = models.EmailField(max_length=32,verbose_name="邮箱")
    name = models.CharField(max_length=32,verbose_name="姓名")
    classname = models.CharField(max_length=64,verbose_name="备注")
    create_time = models.DateTimeField(auto_now=True,verbose_name="创建时间")
    phone = models.CharField(max_length=11, unique=True,verbose_name="手机号")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name
        db_table = 'userinfo'


# Create your models here.
class Subject(models.Model):
    """
    课表
    """
    teacher = models.CharField(max_length=32,unique=True,verbose_name="教师")
    subject_title = models.CharField(max_length=32,unique=True,verbose_name="课程名称")
    introduction = models.CharField(max_length=640,verbose_name="课程简介")
    subject_student = models.ManyToManyField(to="UserInfo",verbose_name="所选学生")
    class_name = models.ManyToManyField(to="ClassNames",verbose_name="教室")
    time = models.DateTimeField(auto_now=True,null=True,verbose_name="课程创建时间")
    startime = models.CharField(max_length=32,unique=True,verbose_name="上课时间")

    def __str__(self):
        return self.subject_title

    class Meta:
        verbose_name = "课表"
        verbose_name_plural = verbose_name
        db_table = 'subject'


class ClassNames(models.Model):
    """
    教室管理
    """
    class_name = models.CharField(max_length=32,unique=True,verbose_name="教室")
    user = models.ManyToManyField(to="UserInfo",verbose_name="教室学生")  # 教室学生
    time = models.DateTimeField(auto_now=True,null=True,verbose_name="教室添加时间")  # 添加教室的时间

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = "教室管理"
        verbose_name_plural = verbose_name
        db_table = 'classnames'
        
        
class TecInfo(models.Model):
    """
    教师信息表
    """
    username = models.CharField(max_length=32,unique=True,verbose_name="教师用户名")
    name = models.CharField(max_length=32,verbose_name="教师姓名")
    password = models.CharField(max_length=64,verbose_name="密码")
    sex = models.CharField(max_length=2,verbose_name="性别")
    experience = models.CharField(max_length=32,verbose_name="经历")
    style = models.CharField(max_length=32,verbose_name="授课风格")
    phone = models.CharField(max_length=11, unique=True,verbose_name="手机号")
    subject_title = models.ManyToManyField(to="Subject",verbose_name="课程")  

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "教师信息"
        verbose_name_plural = verbose_name
        db_table = 'tecinfo'
        

