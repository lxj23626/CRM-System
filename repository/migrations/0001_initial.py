# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', default=False, help_text='Designates that this user has all permissions without explicitly assigning them.')),
                ('username', models.CharField(verbose_name='用户名', max_length=32, unique=True, help_text="<a class='btn-link' href='password'>重置密码</a>")),
                ('email', models.EmailField(verbose_name='邮箱', max_length=32, unique=True)),
                ('name', models.CharField(verbose_name='姓名', max_length=64, blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(verbose_name='groups', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group')),
            ],
            options={
                'verbose_name_plural': '员工信息',
                'permissions': (('repository_check_myadmin', '查看每张表里所有的数据'), ('repository_change_myadmin_get', '访问表里每条数据的修改页'), ('repository_change_myadmin_post', '对表里的每条数据进行修改'), ('repository_add_myadmin_get', '可以访问数据增加页'), ('repository_add_myadmin_post', '创建表里的数据')),
            },
        ),
        migrations.CreateModel(
            name='Classlist',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('class_type', models.SmallIntegerField(default=0, choices=[(0, '脱产'), (1, '周末'), (2, '网络班')])),
                ('semester', models.SmallIntegerField(verbose_name='学期')),
            ],
        ),
        migrations.CreateModel(
            name='ContractTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=64)),
                ('content', models.TextField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='课程名称', max_length=64)),
                ('summary', models.TextField(verbose_name='课程简介')),
                ('price', models.IntegerField(verbose_name='课程价格')),
            ],
            options={
                'verbose_name_plural': '课程',
            },
        ),
        migrations.CreateModel(
            name='CustomerFollowUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('content', models.TextField(verbose_name='跟踪内容')),
                ('status', models.SmallIntegerField(choices=[(0, '近期无报名计划'), (1, '一个月内报名'), (2, '2周内内报名'), (3, '已报名')])),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': '客户跟踪记录',
            },
        ),
        migrations.CreateModel(
            name='CustomerInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(verbose_name='姓名', max_length=32)),
                ('contact_type', models.SmallIntegerField(choices=[(0, '手机号'), (1, 'QQ号'), (2, '微信号')])),
                ('contact_num', models.CharField(verbose_name='联系方式', max_length=64, unique=True)),
                ('source_type', models.SmallIntegerField(choices=[(0, 'QQ群'), (1, '51CTO'), (2, '百度推广'), (3, '知乎'), (4, '转介绍'), (5, '其它')])),
                ('consult_content', models.TextField(verbose_name='咨询内容')),
                ('status', models.SmallIntegerField(choices=[(0, '未报名'), (1, '已报名'), (2, '已退学')])),
                ('date', models.DateField()),
                ('consult_courses', models.ManyToManyField(verbose_name='咨询课程', to='repository.Course')),
            ],
            options={
                'verbose_name': '客户信息',
                'verbose_name_plural': '客户信息',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='菜单名', max_length=32, unique=True)),
                ('url_type', models.SmallIntegerField(default=1, choices=[(0, '静态页面'), (1, '动态页面')])),
                ('url', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': '动态菜单',
            },
        ),
        migrations.CreateModel(
            name='PaymentRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('payment_type', models.SmallIntegerField(default=0, choices=[(0, '报名费'), (1, '学费'), (2, '退费')])),
                ('amount', models.IntegerField(verbose_name='费用', default=500)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('consultant', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('title', models.CharField(verbose_name='角色名', max_length=32, unique=True)),
                ('menu', models.ManyToManyField(blank=True, to='repository.Menu')),
            ],
            options={
                'verbose_name_plural': '角色',
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('u', models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('class_grade', models.ManyToManyField(to='repository.Classlist')),
                ('customer', models.OneToOneField(blank=True, null=True, related_name='stu', to='repository.CustomerInfo')),
            ],
        ),
        migrations.CreateModel(
            name='StudentEnrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('contract_agreed', models.BooleanField(default=False)),
                ('contract_signed_date', models.DateTimeField(blank=True, null=True)),
                ('contract_approved', models.BooleanField(default=False)),
                ('contract_approved_date', models.DateTimeField(verbose_name='合同审核时间', blank=True, null=True)),
                ('enrollment_link', models.CharField(verbose_name='注册链接', max_length=64, blank=True, null=True)),
                ('class_grade', models.ForeignKey(to='repository.Classlist')),
                ('consultant', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(to='repository.CustomerInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('u', models.OneToOneField(default=1, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='paymentrecord',
            name='enrollment',
            field=models.ForeignKey(to='repository.StudentEnrollment'),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('title', 'url')]),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='consultant',
            field=models.ForeignKey(verbose_name='课程顾问', to='repository.Sale'),
        ),
        migrations.AddField(
            model_name='customerinfo',
            name='referral_from',
            field=models.ForeignKey(verbose_name='转介绍', blank=True, null=True, to='repository.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='customerfollowup',
            name='customer',
            field=models.ForeignKey(default=1, to='repository.CustomerInfo'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='contract_template',
            field=models.ForeignKey(blank=True, null=True, to='repository.ContractTemplate'),
        ),
        migrations.AddField(
            model_name='classlist',
            name='course',
            field=models.ForeignKey(to='repository.Course'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ManyToManyField(verbose_name='角色', blank=True, to='repository.Role'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user_permissions',
            field=models.ManyToManyField(verbose_name='user permissions', blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission'),
        ),
        migrations.AlterUniqueTogether(
            name='studentenrollment',
            unique_together=set([('customer', 'class_grade')]),
        ),
        migrations.AlterUniqueTogether(
            name='classlist',
            unique_together=set([('course', 'class_type', 'semester')]),
        ),
    ]
