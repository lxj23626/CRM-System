from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, User
from django.utils.safestring import mark_safe


class UserProfileManager(BaseUserManager):
    ''' 重写shell注册用户方法 '''

    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError('用户名必须填写！')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=32, unique=True, verbose_name='用户名', help_text=mark_safe('''<a class='btn-link' href='password'>重置密码</a>'''))
    email = models.EmailField(max_length=32, unique=True, verbose_name='邮箱')
    role = models.ManyToManyField('Role', verbose_name='角色', blank=True)
    name = models.CharField(max_length=64, verbose_name='姓名', null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    # is_superuser = models.BooleanField(default=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'     # 登录时的唯一认证标识
    REQUIRED_FIELDS = ['email', ]   # 必须填写的字段

    def get_short_name(self):       # 必带，前端页面要用到，不带会报错
        return self.username

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = '员工信息'

        permissions = (
            ('repository_check_myadmin', '查看每张表里所有的数据'),
            ('repository_change_myadmin_get', '访问表里每条数据的修改页'),
            ('repository_change_myadmin_post', '对表里的每条数据进行修改'),
            ('repository_add_myadmin_get', '可以访问数据增加页'),
            ('repository_add_myadmin_post', '创建表里的数据'),

        )


class Sale(models.Model):
        u = models.OneToOneField('UserProfile', default=1)

        def __str__(self):
            return self.u.name


class Teacher(models.Model):
        u = models.OneToOneField('UserProfile', default=1)

        def __str__(self):
            return self.u.name


class Role(models.Model):
    title = models.CharField(max_length=32, unique=True, verbose_name='角色名')
    menu = models.ManyToManyField('Menu', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '角色'


class Menu(models.Model):
    title = models.CharField(max_length=32, unique=True, verbose_name='菜单名')
    url_type_choices = ((0, '静态页面'), (1, '动态页面'))
    url_type = models.SmallIntegerField(choices=url_type_choices, default=1)
    url = models.CharField(max_length=128)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('title', 'url')
        verbose_name_plural = '动态菜单'


class CustomerInfo(models.Model):
    name = models.CharField(max_length=32, verbose_name='姓名')

    contact_tpye_choices = ((0, '手机号'), (1, 'QQ号'), (2, '微信号'))
    contact_type = models.SmallIntegerField(choices=contact_tpye_choices)
    contact_num = models.CharField(max_length=64, unique=True, verbose_name='联系方式')

    source_type_choices = (
        (0, 'QQ群'),
        (1, '51CTO'),
        (2, '百度推广'),
        (3, '知乎'),
        (4, '转介绍'),
        (5, '其它'),
    )
    source_type = models.SmallIntegerField(choices=source_type_choices)
    referral_from = models.ForeignKey('self', blank=True, null=True, verbose_name='转介绍')

    consult_courses = models.ManyToManyField('Course', verbose_name='咨询课程')
    consult_content = models.TextField(verbose_name='咨询内容')
    consultant = models.ForeignKey('Sale', verbose_name='课程顾问')

    status_choices = ((0, '未报名'), (1, '已报名'), (2, '已退学'))
    status = models.SmallIntegerField(choices=status_choices)

    date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = '客户信息'


class Course(models.Model):
    title = models.CharField(max_length=64, verbose_name='课程名称')
    summary = models.TextField(verbose_name='课程简介')
    price = models.IntegerField(verbose_name='课程价格')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = '课程'


class CustomerFollowUp(models.Model):
    """客户跟踪记录表"""
    customer = models.ForeignKey('CustomerInfo', default=1)
    content = models.TextField(verbose_name="跟踪内容")

    status_choices = (
        (0, '近期无报名计划'),
        (1, '一个月内报名'),
        (2, '2周内内报名'),
        (3, '已报名'),
    )
    status = models.SmallIntegerField(choices=status_choices)

    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = '客户跟踪记录'

    def __str__(self):
        return '%s的跟踪内容' %(self.customer,)


class Student(models.Model):
    customer = models.OneToOneField('CustomerInfo',related_name='stu', blank=True, null=True)
    class_grade = models.ManyToManyField('Classlist')

    def __str__(self):
        return self.customer.name


class Classlist(models.Model):
    course = models.ForeignKey('Course')
    class_type_choices = ((0,'脱产'),(1,'周末'),(2,'网络班'))
    class_type = models.SmallIntegerField(choices=class_type_choices,default=0)
    semester = models.SmallIntegerField(verbose_name="学期")
    contract_template = models.ForeignKey("ContractTemplate",blank=True,null=True)

    def __str__(self):
        return '%s(%s)期'%(self.course.title, self.semester)

    class Meta:
        unique_together = ('course', 'class_type', 'semester')


class ContractTemplate(models.Model):
    """存储合同模板"""
    name = models.CharField(max_length=64)
    content = models.TextField()

    date = models.DateField(auto_now_add=True)


class StudentEnrollment(models.Model):
    """学员报名表"""
    customer = models.ForeignKey("CustomerInfo")
    class_grade = models.ForeignKey("Classlist")
    consultant = models.ForeignKey("UserProfile")
    contract_agreed = models.BooleanField(default=False)
    contract_signed_date = models.DateTimeField(blank=True,null=True)
    contract_approved = models.BooleanField(default=False)
    contract_approved_date =  models.DateTimeField(verbose_name="合同审核时间", blank=True, null=True)
    enrollment_link = models.CharField(max_length=64, verbose_name='注册链接', blank=True, null=True)

    class Meta:
        unique_together = ('customer','class_grade')

    def __str__(self):
        return "%s" % self.customer


class PaymentRecord(models.Model):
    """存储学员缴费记录"""
    enrollment = models.ForeignKey(StudentEnrollment)
    payment_type_choices = ((0,'报名费'),(1,'学费'),(2,'退费'))
    payment_type =  models.SmallIntegerField(choices=payment_type_choices,default=0)
    amount = models.IntegerField("费用",default=500)
    consultant = models.ForeignKey("UserProfile")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % self.enrollment



