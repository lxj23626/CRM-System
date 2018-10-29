from repository import models

def view_my_own_customers(request):

    # print(models.UserProfile.objects.filter(sale=1).all())
    # print(request.user.sale)    # 销售b
    # print(1111, request.user.is_superuser)
    if request.user.is_superuser:
        print('钩子函数：超级管理员，放行')
        return True

    # elif models.Sale.objects.filter(id=request.GET.get('consultant'), u=request.user.id):     # consultant = 5，只能看自己的客户

    sale_obj = models.Sale.objects.filter(u=request.user.id)
    customer_obj = models.CustomerInfo.objects.filter(consultant=sale_obj).all()
    print(customer_obj)
    # elif models.Sale.objects.filter(u=request.user.id):  # consultant = 5，只能看自己的客户
    if customer_obj:
        # elif str(request.user.sale.id) == '3':
        print('钩子函数：该用户匹配，放行')
        return True
