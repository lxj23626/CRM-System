from utils.permission_hook import view_my_own_customers
from repository import models

perm_dic = {
    'repository_check_myadmin':['models_data', 'GET', [], {}, ],           # 查看每张表里所有的数据
    'repository_change_myadmin_get': ['change_page', 'GET', [], {}],       # 访问表里每条数据的修改页
    'repository_change_myadmin_post': ['change_page', 'POST', [], {}],     # 对表里的每条数据进行修改
    'repository_add_myadmin_get': ['create_page', 'GET', [], {}],          # 可以访问数据增加页
    'repository_add_myadmin_post': ['create_page', 'POST', [], {}],        # 创建表里的数据

}

#### kwargs只能做些简单操作，不能根据每个人的id查看每个人的客户，要在钩子函数里定义