from django.conf.urls import url, include
from Myadmin import views, account

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/', account.acc_login),
    url(r'^logout/', account.acc_logout),
    url(r'^app/$', views.app_index, name='app_index'),
    url(r'^(\w+)/(\w+)/$', views.models_data, name='models_data'),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.change_page, name='change_page'),
    url(r'^(\w+)/(\w+)/add/$', views.create_page, name='create_page'),
    url(r'^(\w+)/(\w+)/(\d+)/delete/$', views.delete_page, name='delete_page'),
    url(r'^stu_enrollment/', views.stu_enrollment, name='stu_enrollment'),
    

]