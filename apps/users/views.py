# encoding: utf-8
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend

# 并集运算
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from django.shortcuts import render
from django.views.generic.base import View

from users.forms import LoginForm, RegisterForm, ActiveForm
from users.models import UserProfile, EmailVerifyRecord
from utils.email_send import send_register_eamil


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 不希望用户存在两个，get只能有一个。两个是get失败的一种原因 Q为使用并集查询

            user = UserProfile.objects.get(Q(username=username) | Q(email=username))

            # django的后台中密码加密：所以不能password==password
            # UserProfile继承的AbstractUser中有def check_password(self, raw_password):

            if user.check_password(password):
                return user
        except Exception as e:
            print(e)
            return None


# 当我们配置url被这个view处理时，自动传入request对象.
# def user_login(request):
#     # 前端向后端发送的请求方式: get 或post
#     # 登录提交表单为post
#     if request.method == "POST":
#         # 取不到时为空，username，password为前端页面name值
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         # 成功返回user对象,失败返回null
#         user = authenticate(username=user_name, password=pass_word)
#         # 如果不是null说明验证成功
#         if user is not None:
#             # login_in 两参数：request, user
#             # 实际是对request写了一部分东西进去，然后在render的时候：
#             # request是要render回去的。这些信息也就随着返回浏览器。完成登录
#             login(request, user)
#             # 跳转到首页 user request会被带回到首页
#             return render(request, "index.html")
#         # 没有成功说明里面的值是None，并再次跳转回主页面
#         else:
#             return render(request, "login.html", {"msg": "用户名或密码错误!"})
#     # 获取登录页面为get
#     elif request.method == "GET":
#         # render就是渲染html返回用户
#         # render三变量: request 模板名称 一个字典写明传给前端的值
#         return render(request, "login.html", {})
# 基于类实现需要继承的view


class LoginView(View):
    # 直接调用get方法免去判断
    def get(self, request):
        # render就是渲染html返回用户
        # render三变量: request 模板名称 一个字典写明传给前端的值
        return render(request, "login.html", {})

    def post(self, request):
        # 取不到时为空，username，password为前端页面name值
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")

            # 成功返回user对象,失败返回null
            user = authenticate(username=user_name, password=pass_word)

            # 如果不是null说明验证成功
            if user is not None:
                # 只有当用户激活时才给登录
                if user.is_active:
                    # login_in 两参数：request, user
                    # 实际是对request写了一部分东西进去，然后在render的时候：
                    # request是要render回去的。这些信息也就随着返回浏览器。完成登录
                    login(request, user)
                    # 跳转到首页 user request会被带回到首页
                    return render(request, "index.html")
                # 即用户未激活跳转登录，提示未激活
                else:
                    return render(request, "login.html", {"msg": "用户名未激活! 请前往邮箱进行激活"})
            # 没有成功说明里面的值是None，并再次跳转回主页面
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误! "})
        else:
            return render(
                request, "login.html", {
                    "login_form": login_form})


# 注册功能的view
class RegisterView(View):
    # get方法直接返回页面
    def get(self, request):
        # 添加验证码
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        # 实例化form
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 这里注册时前端的name为email
            user_name = request.POST.get("email", "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")

            # 实例化一个user_profile对象，将前台值存入
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            # 默认激活状态为false
            user_profile.is_active = False
            # 加密password进行保存
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 发送注册激活邮件
            send_register_eamil(user_name, "register")
            # 跳转到登录页面
            return render(request, "login.html", {"msg": "请先前往邮箱进行激活"})
        # 注册邮箱form验证失败
        else:
            return render(request, "register.html", {"register_form": register_form})


# 激活用户的view
class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code)
        # 激活form负责给激活跳转进来的人加验证码
        active_form = ActiveForm(request.GET)
        # 如果不为空也就是有用户
        if all_record:
            for record in all_record:
                # 获取到对应的邮箱
                email = record.email
                # 查找到邮箱对应的user
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                # 激活成功跳转到登录页面
                return render(request, "login.html", )
        # 自己瞎输的验证码
        else:
            return render(request, "register.html", {"msg": "您的激活链接无效", "active_form": active_form})
