from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
import time, datetime, os, json
from django import conf
from repository import models
from django.db.models import Q
from utils.find_app import find_app_func
from utils.create_form import create_model_form
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.utils import IntegrityError
from utils.permission import check_permission

# Create your views here.
a = find_app_func()  # 找各个app下的myadmin并自动执行

from utils.site import site
# print(111, site.enabled_admins_dict)
'''site.enabled_admins_dict = 
    {'repository': 
        {
        'userprofile': <utils.base_admin.BaseMyAdmin object at 0x0000027BF2BAFD30>, 
        'role': <utils.base_admin.BaseMyAdmin object at 0x0000027BF2BAFF60>, 
        'menu': <utils.base_admin.BaseMyAdmin object at 0x0000027BF2BAFF98>, 
        'customerinfo': <repository.myadmin.CustomerAdmin object at 0x0000027BF2BC20F0>, 
        'course': <utils.base_admin.BaseMyAdmin object at 0x0000027BF2BC2160>, 
        'customerfollowup': <utils.base_admin.BaseMyAdmin object at 0x0000027BF2BC2208>, 
        'sale': <utils.base_admin.BaseMyAdmin object at 0x0000027BF2BC2278>, 
        'teacher': <utils.base_admin.BaseMyAdmin object at 0x0000027BF2BC22B0>
        }
    }
'''


@login_required
def index(request):
    # 左侧菜单
    role_list = request.user.role.all()     # <QuerySet [<Role: 管理员>]>
    menu_list = models.Menu.objects.filter(role__in=role_list).all().distinct()     # <QuerySet [<Menu: 我的首页>, <Menu: 我的客户库>, <Menu: 我的课程>, <Menu: 我的APP>, <Menu: 学员报名>]>

    # main
    date = datetime.datetime.now()

    return render(request, 'index.html', {'date':date, 'menu_list': menu_list})


@login_required
def app_index(request):
    # 左侧菜单
    role_list = request.user.role.all()
    menu_list = models.Menu.objects.filter(role__in=role_list).all().distinct()

    return render(request, 'app_index.html', {'site':site, 'menu_list': menu_list})


@check_permission
def models_data(request, app_name, model_name):
    print(111, app_name, model_name)
    #### 左侧菜单
    role_list = request.user.role.all()
    menu_list = models.Menu.objects.filter(role__in=role_list).all().distinct()

    #### 展示数据
    admin_class_obj = site.enabled_admins_dict[app_name][model_name]
    data_list = admin_class_obj.model.objects.filter().order_by('-id').all()

    #### 搜索
    search_data = request.GET.get('_search', '')
    admin_class_obj.search_data = search_data       # 输入的要搜索的数据

    if search_data:
        q = Q()     # Q查询
        q.connector = 'OR'

        for search_str in admin_class_obj.search_fields:    # 'contact_num','consultant__u__name'
            q.children.append(('%s__contains'%search_str, search_data))    # 必须传入一个参数（元祖）
        # print(111, q)       # (OR: ('contact_num__contains', 'aaa'), ('consultant__u__name__contains', 'aaa'))
        data_list = data_list.filter(q)

    #### 筛选过滤
    filter_data = request.GET   # 所有get方式传过来的参数：<QueryDict: {'source_type': [''], 'consultant': [''], 'status': [''], 'consult_courses': [''], 'date__gte': [''], '_search': ['']}>
    filter_data_dict = {}
    for k,v in filter_data.items():
        if k in ('_search', '_order', '_page'):
            continue
        elif v:
            filter_data_dict[k] = v

    admin_class_obj.filter_data_dict = filter_data_dict
    data_list = data_list.filter(**filter_data_dict)
    
    #### 单个排序
    order_data = request.GET.get('_order')
    current_ordered_dict = {}
    if order_data:
        order_key = admin_class_obj.list_display[abs(int(order_data))]  # 拿到字符串：'id','name','source_type'....
        current_ordered_dict[order_key] = order_data                    # 记录当前的值

        if order_data.startswith('-'):
            order_key = '-%s' %order_key                                # '-id', '-name'....

        data_list = data_list.order_by('%s'%order_key)
    admin_class_obj.current_ordered_dict = current_ordered_dict
    data_num = data_list.count()

    #### 分页
    paginator = Paginator(data_list, admin_class_obj.list_per_page)
    page_data = request.GET.get('_page')

    try:
        data_list = paginator.page(page_data)                           # 展示输入的页码的数据
    except PageNotAnInteger:
        data_list = paginator.page(1)                                   # 展示第一页的数据
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)                 # paginator.num_pages：总页数

    # print(222, data_list)     # 没传数据：<Page 1 of 5>；传数据2：<Page 2 of 5>；传数据1或者非数字：没有值

    return render(request, 'model_data.html', 
                  {
                      'menu_list': menu_list,
                      'app_name':app_name, 
                      'model_name':model_name, 
                      'admin_class_obj':admin_class_obj,
                      'data_list':data_list,
                      'data_num':data_num,
                  })

@check_permission
def change_page(request, app_name, model_name, obj_id):
    ''' 修改页 '''
    role_list = request.user.role.all()
    menu_list = models.Menu.objects.filter(role__in=role_list).all().distinct()
    
    admin_class_obj = site.enabled_admins_dict[app_name][model_name]
    
    model_form = create_model_form(admin_class_obj)         # 根据Model动态生成一个Form类
    obj = admin_class_obj.model.objects.filter(id=obj_id).first()

    if request.method == 'GET':
        form_obj = model_form(instance=obj)                     # 根据Form类生成一个实例，并赋初始值
    else:
        form_obj = model_form(instance=obj, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/myadmin/%s/%s'%(app_name, model_name))
    return render(request, 'change.html',
                  {
                      'site': site,
                      'menu_list': menu_list,
                      'app_name': app_name,
                      'model_name': model_name,
                      'admin_class_obj': admin_class_obj,
                      'form_obj':form_obj,

                  })

@check_permission
def create_page(request, app_name, model_name):
    ''' 添加页 '''
    role_list = request.user.role.all()
    menu_list = models.Menu.objects.filter(role__in=role_list).all().distinct()

    admin_class_obj = site.enabled_admins_dict[app_name][model_name]
    model_form = create_model_form(admin_class_obj)     # 根据Model动态生成一个Form类

    if request.method == 'GET':
        form_obj = model_form()             # 根据Form类生成一个实例
    else:
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/myadmin/%s/%s' % (app_name, model_name))

    return render(request, 'create.html',
                  {
                      'menu_list': menu_list,
                      'app_name': app_name,
                      'model_name': model_name,
                      'admin_class_obj': admin_class_obj,
                      'form_obj': form_obj,

                  })

# @check_permission
def delete_page(request, app_name, model_name, obj_id):
    ''' 删除页 '''
    admin_class_obj = site.enabled_admins_dict[app_name][model_name]
    obj = admin_class_obj.model.objects.filter(id=obj_id).first()

    if request.method == 'POST':
        obj.delete()
        return redirect('/myadmin/{app_name}/{model_name}/'.format(app_name=app_name, model_name=model_name))
    return render(request, 'delete.html', 
                  {
                      'admin_class_obj':admin_class_obj,
                      'app_name':app_name,
                      'model_name':model_name,
                      'obj':obj,
                  })


# @check_permission
def stu_enrollment(request):
    ''' 学员注册页 '''

    role_list = request.user.role.all()
    menu_list = models.Menu.objects.filter(role__in=role_list).all().distinct()

    customers = models.CustomerInfo.objects.all()
    class_lists = models.Classlist.objects.all()
    enrollment_link = ''

    # enrollment_link = models.StudentEnrollment.objects.filter()

    if request.method == "POST":
        customer_id = request.POST.get("customer_id")
        class_grade_id = request.POST.get("class_grade_id")

        try:
            enrollment_obj = models.StudentEnrollment.objects.create(
                customer_id=customer_id,
                class_grade_id=class_grade_id,
                consultant_id=request.user.id,
            )
        except IntegrityError:     # StudentEnrollment表里已经有这条记录了
            enrollment_obj = models.StudentEnrollment.objects.get(customer_id=customer_id, class_grade_id=class_grade_id)
            if enrollment_obj.contract_agreed:      # 如果同意协议
                return redirect("/stu_enrollment/%s/contract_audit/" %enrollment_obj.id)

        enrollment_link = "http://localhost:8000/enrollment/%s/" %enrollment_obj.id

    return render(request, 'stu_enrollment.html',
                  {
                      'menu_list': menu_list,
                      'customers':customers,
                      'class_lists':class_lists,
                      'enrollment_link':enrollment_link,
                  })


from utils.enrollment_form import CustomerForm
def enrollment(request, enrollment_id):
    """学员在线报名表地址"""

    enrollment_obj = models.StudentEnrollment.objects.get(id=enrollment_id)
    # customer_form = ''

    if enrollment_obj.contract_agreed:
        return HttpResponse("报名合同正在审核中....")

    if request.method == 'GET':
        customer_form = CustomerForm(instance=enrollment_obj.customer)
    elif request.method == "POST":
        customer_form = CustomerForm(instance=enrollment_obj.customer, data=request.POST)
        if customer_form.is_valid():
            print(333, customer_form.cleaned_data)
            # customer_form.save()
            enrollment_obj.contract_agreed = True
            enrollment_obj.contract_signed_date = datetime.datetime.now()
            enrollment_obj.save()
            return HttpResponse("您已成功提交报名信息,请等待审核通过")


    #### 列出已上传文件
    uploaded_files = []
    enrollment_upload_dir = os.path.join(conf.settings.FILE_UPLOAD_DIR, enrollment_id)
    if os.path.isdir(enrollment_upload_dir):
        uploaded_files = os.listdir(enrollment_upload_dir)

    return render(request, 'enrollment.html', {'customer_form':customer_form, 'enrollment_obj':enrollment_obj, 'uploaded_files':uploaded_files})


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def enrollment_fileupload(request, enrollment_id):
    ''' 文件上传 '''
    ret = {'status':True, 'err_msg':None}

    enrollment_upload_dir = os.path.join(conf.settings.FILE_UPLOAD_DIR, enrollment_id)
    if not os.path.isdir(enrollment_upload_dir):
        os.mkdir(enrollment_upload_dir)     # 创建enrollment_id=1的文件夹

    file_obj = request.FILES.get('file')

    if len(os.listdir(enrollment_upload_dir))< 2:      # os.listdir(enrollment_upload_dir：把该文件夹下所有的文件名放入一个列表
        with open(os.path.join(enrollment_upload_dir,file_obj.name), "wb") as f:
            for chunks in file_obj.chunks():
                f.write(chunks)
    else:
        ret['status'] = False
        ret['err_msg'] = '上传文件不能大于2个'

    return HttpResponse(json.dumps(ret))


def contract_audit(request, enrollment_id):
    return HttpResponse('已提交申请，请等待审核')