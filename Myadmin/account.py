from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout


def acc_login(request):
    err_msg = ''
    next_url = request.GET.get('next','/myadmin')
    # print(222, next_url)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        # print(111,user)
        if user:
            login(request, user)

            return redirect(next_url)

        else:
            err_msg = '用户名或密码错误！'

    return render(request, 'login.html',{'err_msg':err_msg})


def acc_logout(request):
    logout(request)
    
    return redirect('/myadmin')