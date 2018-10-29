from django.forms import ModelForm

def create_model_form(admin_class_obj):
    ''' 动态生成form '''

    # 根据Model动态生成Form表单
    class Meta:
        model = admin_class_obj.model
        fields = '__all__'

    # 自定义form样式
    def __new__(cls, *args, **kwargs):
        # print(111,cls.base_fields)
        '''cls.base_fields =
        OrderedDict(
            [
                ('name', <django.forms.fields.CharField object at 0x00000244C6469470>),
                ('contact_type', <django.forms.fields.TypedChoiceField object at 0x00000244C6480588>),
                ('contact_num', <django.forms.fields.CharField object at 0x00000244C6480828>),
                ('source_type', <django.forms.fields.TypedChoiceField object at 0x00000244C6480978>),
                ('referral_from', <django.forms.models.ModelChoiceField object at 0x00000244C6480908>),
                ('consult_courses', <django.forms.models.ModelMultipleChoiceField object at 0x00000244C64809E8>),
                ('consult_content', <django.forms.fields.CharField object at 0x00000244C6480B70>),
                ('consultant', <django.forms.models.ModelChoiceField object at 0x00000244C6480CF8>),
                ('status', <django.forms.fields.TypedChoiceField object at 0x00000244C6480E48>),
                ('date', <django.forms.fields.DateField object at 0x00000244C6480F28>)
            ]
        )
        '''
        for field_name in cls.base_fields:
            # print(field_name)   # name, contact_type, contact_num....
            # print(cls.base_fields['name'])    # <django.forms.fields.CharField object at 0x00000244C6469470>

            cls.base_fields[field_name].widget.attrs.update({'class':'form-control'})     # 给每个字段加属性
            if field_name == 'contact_num':
                cls.base_fields[field_name].error_messages = {'required':'标签名不能为空'}

        return ModelForm.__new__(cls)


    dynamic_model_form = type('DModelForm', (ModelForm,), {'Meta':Meta, '__new__':__new__})

    return dynamic_model_form