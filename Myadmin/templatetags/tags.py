from django.template import Library
from django.utils.safestring import mark_safe
import datetime

register = Library()

@register.simple_tag()
def get_model_verbose_name(admin_class_obj):
    # 获取表的别名
    return admin_class_obj.model._meta.verbose_name


@register.simple_tag()
def get_item(admin_class_obj, data):
    ''' 处理要展示的数据 '''

    ele = ''
    if admin_class_obj.list_display:
        for index, item in enumerate(admin_class_obj.list_display):
            item_obj = admin_class_obj.model._meta.get_field(item)     # 通过字符串在表中获取相应的【字段对象】，为了看这张表里的字段是否有choice，与创建的数据无关
            if item_obj.choices:
                item_data = getattr(data, 'get_%s_display'%item)()
            else:
                item_data = getattr(data, item)     # 通过字符串在每条【数据】里获取相应的【对象】，如：'id', 'name', 'status'
            
            td_ele = "<td>%s</td>" % item_data
            if admin_class_obj.list_display[index] == 'name':
                td_ele = "<td><a href='%s/change/'>%s</a></td>"%(data.id, item_data)

            ele += td_ele
    else:
        td_ele = "<td><a href='%s/change/'>%s</a></td>" % (data.id, data)
        ele += td_ele
    return mark_safe(ele)


@register.simple_tag()
def get_filter_item(admin_class_obj, list_filter_str):
    ''' 处理要过滤的数据 '''

    ele = ''
    list_filter_obj = admin_class_obj.model._meta.get_field(list_filter_str)    # 根据字段字符串获取字段对象

    if list_filter_str == 'date':
        time_obj = datetime.date.today()        # 仅获取今天的日期

        time_options_list = [
            ('', '---------'),
            (time_obj, '今天'),
            (time_obj - datetime.timedelta(7), '7天内'),
            (time_obj.replace(day=1), '本月内'),
            (time_obj - datetime.timedelta(90), '3个月内'),
            (time_obj.replace(month=1, day=1), '本年内'),
        ]

        for option_item in time_options_list:
            selected = ''
            if 'date__gte' in admin_class_obj.filter_data_dict:     # 如果'date__gte'在筛选字典里
                if admin_class_obj.filter_data_dict['date__gte'] == str(option_item[0]):     # 如果这个字段在筛选字典里且等于这个数字
                    # print(111, str(option_item[0]))       # 2018-08-18
                    selected = 'selected'
            option_ele = '<option %s value="%s">%s</option>'%(selected, option_item[0], option_item[1])
            ele += option_ele

    else:
        for option_item in list_filter_obj.get_choices():               # get_choices()：获取表里的字段的每个选项
            # print(222, option_item)
            selected = ''
            if list_filter_str in admin_class_obj.filter_data_dict:     # 如果这个字段在筛选字典里
                if admin_class_obj.filter_data_dict[list_filter_str] == str(option_item[0]):     # 如果这个字段在筛选字典里且等于这个数字
                    # print(111, str(option_item[0]))
                    selected = 'selected'
            option_ele = '<option %s value="%s">%s</option>'%(selected, option_item[0], option_item[1])

            ele += option_ele

    return mark_safe(ele)

# 
# def order_num(admin_class_obj, forloop_counter0):
#     ''' 生成order序号标签 '''
#     
#     if not admin_class_obj['order']:
#         ele = '?_order=%s' %forloop_counter0
#     else:

@register.simple_tag()
def order_title(admin_class_obj):
    ''' 生成小标题 '''
    ele = ''

    for index, i in enumerate(admin_class_obj.list_display):
        this_order = index
        arrow = ''
        if i in admin_class_obj.current_ordered_dict:
            last_order = admin_class_obj.current_ordered_dict[i]

            if last_order.startswith('-'):
                this_order = last_order.strip('-')
                arrow = '<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>'
            else:
                this_order = '-%s' %last_order
                arrow = '<span class="glyphicon glyphicon-triangle-top" aria-hidden="true"></span>'

        filter_str = joint_filter_str(admin_class_obj)
        search_str = joint_search_str(admin_class_obj)

        th_ele = '<th><a href="?_order=%s%s%s"> %s %s </a></th>' % (this_order, filter_str, search_str, i, arrow)
        ele += th_ele

    return mark_safe(ele)


@register.simple_tag()
def joint_filter_str(admin_class_obj):
    ''' 筛选过滤字段 '''

    filter_str = ''
    if admin_class_obj.filter_data_dict:
        for k, v in admin_class_obj.filter_data_dict.items():
            filter_str += '&%s=%s' % (k, v)

    return filter_str


@register.simple_tag()
def joint_search_str(admin_class_obj):
    ''' 搜索字段 '''

    search_str = ''
    if admin_class_obj.search_data:
        search_str = '&_search=%s' % (admin_class_obj.search_data)

    return search_str

@register.simple_tag()
def joint_order_str(admin_class_obj):
    ''' 筛选排序字段 '''

    order_str = ''
    if admin_class_obj.current_ordered_dict:
        for k, v in admin_class_obj.current_ordered_dict.items():
            order_str = '&_order=%s' % (v,)

    return order_str

        
@register.simple_tag()
def page_handle(admin_class_obj, data_list):
    ele = '<ul class="pagination">'

    # 上一页
    if data_list.has_previous():
        pre = '<li><a href="?_page=%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'%(data_list.previous_page_number(),)
    else:
        pre = '<li class="disabled"><span aria-hidden="true">&laquo;</span></li>'
    ele += pre

    for i in data_list.paginator.page_range:
        if abs(data_list.number-i) < 4:
            active = ''
            if data_list.number == i:
                active = 'active'

            filter_str = joint_filter_str(admin_class_obj)
            search_str = joint_search_str(admin_class_obj)
            order_str = joint_order_str(admin_class_obj)

            p_ele = '''<li class="%s"><a href="?_page=%s%s%s%s">%s</a></li>''' % (active, i, filter_str, search_str, order_str, i)
            ele += p_ele

    # 下一页
    if data_list.has_next():
        nex = '<li><a href="?_page=%s" aria-label="Previous"><span aria-hidden="true">»</span></a></li>' % (data_list.next_page_number(),)
    else:
        nex = '<li class="disabled"><span aria-hidden="true">»</span></li>'
    ele += nex
    ele += "</ul>"

    return mark_safe(ele)

@register.simple_tag()
def get_mul_select_option(field_name, form_obj, admin_class_obj):
    ''' 获取M2M字段的option '''
    field_obj = admin_class_obj.model._meta.get_field(field_name)   # repository.CustomerInfo.consult_courses：CustomerInfo类的consult_courses字段对象
    # print(111, field_obj.related_model)                           # <class 'repository.models.Course'>：与之相关联的Course类
    # print(111, field_obj.related_model.objects.all())             # 获取所有Course的数据：<QuerySet [<Course: Python>, <Course: Java>, <Course: Linux>, <Course: GoLang>]>
    # print(111, form_obj.instance)                                 # 获取当前操作的对象：客户15
    # print(111, getattr(form_obj.instance, field_name).all())      # 已选的：<QuerySet [<Course: Java>, <Course: GoLang>, <Course: Python>]>

    #### 获取所有可选的字段
    obj_list = set(field_obj.related_model.objects.all())
    
    if form_obj.instance.id:    # 如果是修改页
        # 获取该instance对象选中的字段
        selected_list = set(getattr(form_obj.instance, field_name).all())   
        
        return obj_list-selected_list   # 返回该instance对象没选的字段
    else:
        return obj_list

@register.simple_tag()
def get_selected_option(field_name, form_obj, admin_class_obj):
    ''' 获取已选的M2M字段的option '''
    if form_obj.instance.id:
        selected_list = getattr(form_obj.instance, field_name).all()
        
        return selected_list
    else:
        return []

@register.simple_tag()
def display_all_related_objs(obj):                  # obj = 客户8

    ele = '<div>'
    # print(1111, obj._meta.related_objects)      # 根据一条数据对象obj找到所有被ForeignKey的model和被ManyToManyField的model

    for related_object in obj._meta.related_objects:       # (<ManyToOneRel: repository.customerinfo>, <ManyToOneRel: repository.customerfollowup>, <OneToOneRel: repository.student>, <ManyToOneRel: repository.studentenrollment>)
        ele += '<ul>'
        if related_object.get_internal_type() != 'OneToOneField':
            # print(11111, related_object.name)

            related_objs = getattr(obj, "%s_set" % related_object.name).all()    # 通过reversed_fk_obj.name获取对象的name字符串customerinfo, customerfollowup反向查所有关联的数据
            # print(33333, related_objs)
            # print(666, dir(related_objs),type(related_objs))

        else:
            # try:
            #     print(111, related_object.name)
            #     print(22222, obj.student)
            #     related_objs2 = getattr(obj, related_object.name)
            #     print(555,dir(related_objs2._meta.related_objects),type(related_objs2))
            #     print(3333, related_objs2._meta.all())
            # except Exception as e:
            #     print('error:', e)
            pass

            # related_objs = getattr(obj, '%s.customer'%related_object.name).all()
        # print(123,related_objs)                          # 【客户15】和【客户8的跟踪内容】

        # related_objs_count = related_objs.count()
        # if related_model_name == obj._meta.model_name:
        #     related_objs_count = related_objs_count + 1
        # ele += "<li><b>111%s:</b> %s条<ul> " % (related_model_name, related_objs_count)

        if related_object.get_internal_type() == "ManyToManyField":        # ManyToManyField不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/myadmin/%s/%s/%s/change/'>%s</a> 记录里与【%s】相关的的数据将被删除</li>" %(i._meta.app_label, i._meta.model_name, i.id, i, obj)
        # if related_object.get_internal_type() == "OneToOneField":
        #     pass
        #     ele += "<li>将被删除</li>" %()
        else:
            for i in related_objs:
                print(111, i._meta.model_name)
                ele += "<li><a href='/myadmin/%s/%s/%s/change/'>%s</a>将被删除</li>" %(i._meta.app_label, i._meta.model_name, i.id, i)
                ele += display_all_related_objs(i)
        ele += '</ul>'

    ele += '</div>'

    return mark_safe(ele)


