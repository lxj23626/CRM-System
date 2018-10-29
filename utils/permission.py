from django.core.urlresolvers import resolve
from django.shortcuts import render, HttpResponse, redirect
from utils.permission_list import perm_dic
from django.conf import settings

def check_permission(func):
    def inner(*args, **kwargs):
        # print(222, *args, **kwargs)
        if not perm_check(*args, **kwargs):
            request = args[0]
            # print(111,request)
            return render(request, 'page_403.html')
        return func(*args, **kwargs)
    return inner


def perm_check(*args, **kwargs):
    # print(333, args)        # (<WSGIRequest: GET '/myadmin/repository/customerinfo/'>, 'repository', 'customerinfo')
    request = args[0]
    resolve_url_obj = resolve(request.path)     # 反解url：ResolverMatch(func=utils.permission.inner, args=('repository', 'userprofile'), kwargs={}, url_name=models_data, app_names=[], namespaces=[])
    url_name = resolve_url_obj.url_name         # 当前url的url_name：models_data
    # print('---perm:',request.user, request.user.is_authenticated(), url_name)       # root True models_data
    match_results = [None,]
    match_key = None


    if not request.user.is_authenticated():     # 未登录
         return redirect(settings.LOGIN_URL)

    for permission_key, permission_val in perm_dic.items():
        per_url_name = permission_val[0]
        per_method = permission_val[1]
        perm_args = permission_val[2]
        perm_kwargs = permission_val[3]
        perm_hook_func = permission_val[4] if len(permission_val) > 4 else None

        if per_url_name == url_name:            # 检测url是否匹配
            if per_method == request.method:    # 检测方法是否匹配

                args_matched = False
                for item in perm_args:
                    request_method_func = getattr(request, per_method)  # request.GET/POST
                    if request_method_func.get(item, None):             # 检测request字典中是否有此参数：request.GET.get(item, None)
                        args_matched = True
                    else:
                        args_matched = False
                        # print(444, args_matched)

                        break                                           # 有一个参数不能匹配成功，则判定为假，退出该循环
                else:                   # 当服务端权限字典perm_dic的参数列表perm_args为空的时候才走这里
                    args_matched = True

                kwargs_matched = False
                for k, v in perm_kwargs.items():
                    request_method_func = getattr(request, per_method)
                    arg_val = request_method_func.get(k, None)          # 检测request字典中是否有此参数
                    # print("perm kwargs check:", arg_val, type(arg_val), v, type(v))
                    if arg_val == str(v):       # 匹配上了特定的参数 及对应的 参数值， 比如，需要request 对象里必须有一个叫 user_id=3的参数
                        kwargs_matched = True
                    else:
                        kwargs_matched = False
                        break                   # 有一个参数不能匹配成功，则判定为假，退出该循环
                else:
                    kwargs_matched = True

                # 匹配自定义权限钩子函数
                perm_hook_matched = False
                if perm_hook_func:
                    perm_hook_matched = perm_hook_func(request)
                else:
                    perm_hook_matched = True

                match_results = [args_matched, kwargs_matched, perm_hook_matched]   # [True, True, False]
                # print("--->match_results ", match_results)
                if all(match_results):          # all()：全为真才返回True
                    match_key = permission_key
                    break
    
    if all(match_results):
        app_name, *per_name = match_key.split('_')      # permission_key = match_key = repository_check_myadmin，只要app_name,
        perm_obj = '%s.%s' % (app_name, match_key)      # perm_obj = repository.repository_check_myadmin：表名.权限名
        if request.user.has_perm(perm_obj):
            print('当前用户有此权限')
            return True
        else:
            print('当前用户没有该权限')
            return False
    else:
        print("未匹配到权限项，当前用户无权限")