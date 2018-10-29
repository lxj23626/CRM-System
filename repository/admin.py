from django.contrib import admin
from repository import models
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from repository.models import UserProfile


class UserChangeForm(forms.ModelForm):
    ''' 自定义修改用户页面 '''

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfile
        # fields = ('email', 'password', 'username', 'is_active', 'is_superuser')
        fields = ()


    def clean_password(self):
        return self.initial['password']


class UserCreationForm(forms.ModelForm):
    ''' 自定义创建用户页面 '''

    password1 = forms.CharField(label='密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    # class Meta:
    #     model = UserProfile
    #     fields = ('username', 'email',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("两次密码输入不一致！！")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user



class UserProfileAdmin(UserAdmin):

    form = UserChangeForm
    # add_form = UserCreationForm


    list_display = ('email', 'is_superuser')
    list_filter = ('is_superuser',)
    search_fields = ('email',)
    ordering = ('username',)        # 默认排序


    filter_horizontal = ('user_permissions', 'groups', 'role')

    fieldsets = (                   # 不带会报错，估计是继承了fieldsets
        ('Personal info', {'fields': ('username','name', 'email', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'user_permissions', 'groups')})
    )

    add_fieldsets = (
        ('aaa', {
            'classes': ('wide',),   # label和输入框之间宽一点
            'fields': ('username', 'email', 'password1', 'password2', 'is_active', 'is_superuser', 'is_staff')      # 创建表时要展示的内容
        }),
    )



class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'source_type', 'contact_type', 'contact_num', 'consultant', 'consult_content', 'status', 'date', ]     # 不能显示多对多字段
    list_filter = ['source_type', 'consultant', 'status', 'date']
    # list_filter = ['contact_num',]

    search_fields = ['contact_num', 'consultant__u__name', 'consult_courses__title']

    readonly_fields = ['status', 'contact_num']
    filter_horizontal = ['consult_courses',]
    list_per_page = 2




admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Role)
admin.site.register(models.Menu)
admin.site.register(models.CustomerInfo, CustomerAdmin)
admin.site.register(models.Course)
admin.site.register(models.CustomerFollowUp)
admin.site.register(models.Sale)
admin.site.register(models.Teacher)
admin.site.register(models.Classlist)


