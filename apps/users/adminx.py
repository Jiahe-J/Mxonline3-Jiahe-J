#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
@author:silenthz 
@file: adminx.py 
@time: 2018/02/28 
"""
import xadmin
from django.contrib.auth.models import Group, Permission

from xadmin import views
from xadmin.layout import Main, Row, Fieldset, Side
from xadmin.models import Log
from xadmin.plugins.auth import UserAdmin

from courses.models import Course, Lesson, Video, CourseResource, BannerCourse
from operation.models import CourseComments, UserCourse, UserFavorite, UserMessage, UserAsk
from organization.models import CityDict, Teacher, CourseOrg
from .models import EmailVerifyRecord, Banner, UserProfile


# 创建admin的管理类,这里不再是继承admin，而是继承object
class EmailVerifyRecordAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['email', 'code', 'send_type', 'send_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['code', 'email', 'send_type']
    # 配置筛选字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


# 创建banner的管理类
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


# 创建Xadmin的全局管理器并与view绑定。
class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True


# xadmin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = "玉汝于成: 后台管理站"
    site_footer = "Jihe-J's MOOC"
    # 收起菜单
    menu_style = "accordion"

    def get_site_menu(self):
        return (
            {'title': '课程管理', 'icon': 'fa fa-university', 'menus': (
                {'title': '课程信息', 'icon': 'fa fa-bookmark', 'url': self.get_model_url(Course, 'changelist')},
                {'title': '轮播课程', 'icon': 'fa fa-bookmark-o', 'url': self.get_model_url(BannerCourse, 'changelist')},
                {'title': '章节信息', 'icon': 'fa fa-fire', 'url': self.get_model_url(Lesson, 'changelist')},
                {'title': '视频信息', 'icon': 'fa fa-video-camera', 'url': self.get_model_url(Video, 'changelist')},
                {'title': '课程资源', 'icon': 'fa fa-folder', 'url': self.get_model_url(CourseResource, 'changelist')},
                {'title': '课程评论', 'icon': 'fa fa-comments', 'url': self.get_model_url(CourseComments, 'changelist')},
            )},
            {'title': '机构管理', 'icon': 'fa fa-building', 'menus': (
                {'title': '机构信息', 'icon': 'fa fa-building-o', 'url': self.get_model_url(CourseOrg, 'changelist')},
                {'title': '机构讲师', 'icon': 'fa fa-user-circle-o', 'url': self.get_model_url(Teacher, 'changelist')},
                {'title': '所在城市', 'icon': 'fa fa-location-arrow', 'url': self.get_model_url(CityDict, 'changelist')},
            )},
            {'title': '用户管理', 'icon': 'fa fa-user', 'menus': (
                {'title': '用户信息', 'icon': 'fa fa-user-o', 'url': self.get_model_url(UserProfile, 'changelist')},
                {'title': '用户验证', 'icon': 'fa fa-key', 'url': self.get_model_url(EmailVerifyRecord, 'changelist')},
                {'title': '用户课程', 'icon': 'fa fa-graduation-cap', 'url': self.get_model_url(UserCourse, 'changelist')},
                {'title': '用户收藏', 'icon': 'fa fa-star', 'url': self.get_model_url(UserFavorite, 'changelist')},
                {'title': '用户消息', 'icon': 'fa fa-commenting', 'url': self.get_model_url(UserMessage, 'changelist')},
            )},

            {'title': '系统管理', 'icon': 'fa fa-cogs', 'menus': (
                {'title': '用户咨询', 'icon': 'fa fa-comment-o', 'url': self.get_model_url(UserAsk, 'changelist')},
                {'title': '首页轮播', 'icon': 'fa fa-exchange', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': '用户分组', 'icon': 'fa fa-group', 'url': self.get_model_url(Group, 'changelist')},
                {'title': '用户权限', 'icon': 'fa fa-certificate', 'url': self.get_model_url(Permission, 'changelist')},
                {'title': '日志记录', 'icon': 'fa fa-tasks', 'url': self.get_model_url(Log, 'changelist')},
            )})


# class UserProfileAdmin(UserAdmin):
#     def get_form_layout(self):
#         if self.org_obj:
#             self.form_layout = (
#                 Main(
#                     Fieldset('',
#                              'username', 'password',
#                              css_class='unsort no_title'
#                              ),
#                     Fieldset(_('Personal info'),
#                              Row('first_name', 'last_name'),
#                              'email'
#                              ),
#                     Fieldset(_('Permissions'),
#                              'groups', 'user_permissions'
#                              ),
#                     Fieldset(_('Important dates'),
#                              'last_login', 'date_joined'
#                              ),
#                 ),
#                 Side(
#                     Fieldset(_('Status'),
#                              'is_active', 'is_superuser',
#                              ),
#                 )
#             )
#         return super(UserAdmin, self).get_form_layout()


xadmin.site.register(views.CommAdminView, GlobalSettings)  # 将头部与脚部信息进行注册:
# 将管理器与model进行注册关联
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
# 将全局配置管理与view绑定注册
xadmin.site.register(views.BaseAdminView, BaseSetting)
# xadmin.site.register(UserProfile, UserProfileAdmin)
