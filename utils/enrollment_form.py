from django.forms import ModelForm
from django import forms
from repository import models

# class EnrollmentForm(ModelForm):
#     class Meta:
#         model = models.StudentEnrollment
#         fields = "__all__"
#         exclude = ['contract_approved_date']
#         readonly_fields = ['contract_agreed',]
        
        
class CustomerForm(ModelForm):
    class Meta:
        model = models.CustomerInfo
        #fields = ['name','consultant','status']
        fields = "__all__"
        exclude = ['consult_content','status','consult_courses']
        readonly_fields = ['contact_type','contact_num','consultant','referral_from','source_type']

    def __new__(cls, *args, **kwargs):
        # print(cls,args,kwargs)        # <class 'utils.enrollment_form.CustomerForm'> () {'instance': <CustomerInfo: 客户111111>}
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class':'form-control'})

            if field_name in cls.Meta.readonly_fields:
                filed_obj.widget.attrs.update({'readonly': 'true'})

        return  ModelForm.__new__(cls)

    def clean(self):
        if self.errors:
            raise forms.ValidationError(("Please fix errors before re-submit."))    # 添加__all__全局错误
        if self.instance.id:
            for field in self.Meta.readonly_fields:
                old_field_val = getattr(self.instance, field)    # 数据库里的数据
                form_val = self.cleaned_data.get(field)

                if old_field_val != form_val:       # 在这个字段下面添加一个错误
                    self.add_error(field,"Readonly Field: field should be '{value}' ,not '{new_value}' ".format(**{'value':old_field_val,'new_value':form_val}))
