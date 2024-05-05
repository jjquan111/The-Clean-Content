from django.contrib import admin
from dal import models


admin.site.site_header = 'The Clean Content'
admin.site.site_title = '登录The Clean Content'
admin.site.index_title = 'The Clean Content后台管理'

# Register your models here.


class DetectsAdmin(admin.ModelAdmin):
    list_display = ('id','detectcontent','detectresult')
admin.site.register(models.detects,DetectsAdmin)



class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password','email','name','classname','create_time','phone')

admin.site.register(models.UserInfo, UserAdmin)



