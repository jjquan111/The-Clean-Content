"""study_class URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import path

import study_class.views

from api.route import href_index, href_register, href_login, href_promessage, href_subject, href_select_subject, \
    href_updatepwd, href_teacher, href_select_file, href_line, href_use_cam
from api import register,login,pro_message,pro_subject,add_subject,all_subject,updatemypwd,teacher

urlpatterns = [

    url('uploadwordfile',study_class.views.uploadwordfile),
    url('uploadmainfile',study_class.views.uploadmainfile),
    url('admin/', admin.site.urls),
    # 前台首页
    url(r'index/$', href_index.StudyIndex.as_view()),
    url(r'indextec/$', href_index.TecIndex.as_view()),
    # 学生登录
    url(r'login/$', href_login.Login.as_view()),

    url(r'loginTec/$', href_login.loginTec.as_view()),
    # 注册
    url(r'register/$', href_register.Register.as_view()),
    # 注册接口
    url(r'register/register/create/$', register.Register.as_view()),
    # 登录接口
    url('login/login/auth/$', login.Login.as_view()),
    url('loginTec/logintec/auth/$', login.LoginTec.as_view()),

    url('line/$',href_line.line.as_view()),
    url('main/$',href_line.linemain.as_view()),


    url(r'href/UpdatePwd/$', href_updatepwd.ProUpdatePwd.as_view()),
    url(r'href/UpdatePwdtec/$', href_updatepwd.ProUpdatePwdTec.as_view()),

    url('UpdateMyPwd/$', updatemypwd.UpdateMyPwd.as_view()),    
    url('UpdateMyPwdTec/$', updatemypwd.UpdateMyPwdTec.as_view()),

    url(r'pro/message/$', pro_message.ProMessage.as_view()),
    url(r'pro/messagetec/$', pro_message.ProMessageTec.as_view()),

    url(r'href/subject/$', href_subject.Subject.as_view()),
    url(r'href/subject2/$', href_subject.Subject2.as_view()),
    url(r'href/subjecttec/$', href_subject.SubjectTec.as_view()),
    

    url(r'pro/subject/$', pro_subject.ProSubject.as_view()),
    url(r'pro/subjecttec/$', pro_subject.ProSubjectTec.as_view()),


    url(r'href/select/$', href_select_subject.ProHrefSelect.as_view()),
    url(r'href/select2/$', href_select_subject.ProHrefSelect2.as_view()),
    url(r'href/selectsubject/$', href_select_subject.ProHrefSelectTec.as_view()),
    url(r'href/FileUpdateCam/$', href_use_cam.usecam.as_view()),
    url(r'passageupdate/$', study_class.views.updatepassage,name='submit'),
    url(r'href/FileUpdateJpg/$', study_class.views.updatefilejpg, name='submitjpg'),
    url(r'href/ScreenShow/$', href_select_file.ScreenShow.as_view()),
    

    url(r'subject/$', all_subject.AllSubject.as_view()),
    url(r'subjectquery/$', all_subject.QuerySubject.as_view()),
    

    url(r'pro/TeachInfo/$', href_teacher.Subject.as_view()),

    url(r'TeachInfoAll/$',  teacher.AllTecInfo.as_view()),
    url(r'TeachInfoBySubject/$',  teacher.TeachInfoBySubject.as_view()),
    
    

    url(r'add/$', add_subject.AddSubject.as_view()),
]
