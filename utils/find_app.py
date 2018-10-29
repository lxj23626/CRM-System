from django import conf

def find_app_func():
    ''' 找各个app下的myadmin并自动执行 '''

    for app_name in conf.settings.INSTALLED_APPS:
        try:
            mod = __import__('%s.myadmin' %app_name)
            # print(mod.myadmin)
        except ModuleNotFoundError:
            pass
