from utils.site import site
from repository import models
from utils.base_admin import BaseMyAdmin

class CustomerAdmin(BaseMyAdmin):
    list_display = ['id', 'name', 'source_type', 'contact_type', 'contact_num', 'consultant', 'consult_content', 'status', 'date']
    # list_display = ['date',]

    list_filter = ['source_type','consultant','status', 'consult_courses', 'date']
    # list_filter = ['date',]

    search_fields = ['contact_num', 'consultant__u__name']

    readonly_fields = ['status','contact_num']
    filter_horizontal = ['consult_courses',]
    list_per_page = 3


site.register(models.UserProfile)
site.register(models.Role)
site.register(models.Menu)
site.register(models.CustomerInfo, CustomerAdmin)
site.register(models.Course)
site.register(models.CustomerFollowUp)
site.register(models.Sale)
site.register(models.Teacher)

