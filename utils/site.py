from utils.base_admin import BaseMyAdmin

class AdminSite(object):
    def __init__(self):
        self.enabled_admins_dict = {}

    def register(self, model_class_name, admin_class_name=None):
        ''' 注册admin表 '''

        if not admin_class_name:
            admin_class_name = BaseMyAdmin()
        else:
            admin_class_name = admin_class_name()

        admin_class_name.model = model_class_name

        app_name = model_class_name._meta.app_label     # 通过【model对象】拿到app名的【字符串】
        model_name = model_class_name._meta.model_name  # 通过【model对象】拿到model名的【字符串】

        if app_name not in self.enabled_admins_dict:
            self.enabled_admins_dict[app_name] = {}
        self.enabled_admins_dict[app_name][model_name] = admin_class_name 

site = AdminSite()