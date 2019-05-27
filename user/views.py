from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from user.models import User
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from dailyfresh.settings import SECRET_KEY
from django.core.mail import send_mail
from dailyfresh.settings import EMAIL_FROM
import logging
from django.contrib.auth import authenticate
from django.contrib.auth import login as LOGIN
from celery_tasks.tasks import send_active_mail
from django.contrib.auth.decorators import login_required
class register(View):
    def post(self,request):
        # 1获取 user/pwd/email 文本

        user_name = request.POST['user_name']
        password = request.POST['pwd']
        email = request.POST['email']
        allow = request.POST['allow']

        # 2 格式的校验
        if allow != 'on':
            return render(request, 'register.html', {'errormsg': '没有通过协议'})
        if not all([user_name, password, email, allow]):
            return render(request, 'register.html', {'errormsg': '信息不完整'})

        # 3 注册
        user = User.objects.create_user(user_name, email, password)
        user.is_active = 0
        user.save()
        # 4  激活邮件
            #  （1）注册用户的id 生成加密token

        serializer = Serializer(SECRET_KEY,24*3600*30)
        data = {'confirm':user.id}
        token = serializer.dumps(data).decode()

        send_active_mail.delay(email,token,user_name)
            # 放入任务队列
        aim = reverse('shouye')
        return redirect(aim)


    def get(self,request):
        return  render(request,'register.html')




def active(request,token):
    serializer = Serializer(SECRET_KEY, 24 * 3600 * 30)
    data = serializer.loads(token)
    user_id = data["confirm"]

    user = User.objects.get(id = user_id)
    user.is_active = 1
    user.save()
    # 账号激活完成
    # 登录页面。
    aim = reverse('denglu')
    return redirect(aim)


class login(View):
    def get(self,request): # 访问
        # 判断cookies 里面有没有登录用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES['username']
            checked = 'checked'
        elif 'username' not in request.COOKIES:
            # 没有记住用户名，用户名为空，勾选记住为空
            username = ''
            checked = ''
        return render(request,'login.html',{'username':username,'checked':checked})

    def post(self,request): # 登录

        # 1. 获取 str
        username = request.POST['username']
        password = request.POST['pwd']
        # 2. 验证完整性
        if not all([username,password]):
            return render(request,'login.html',{'errormsg':'数据不完整'})
        # 3. 登录验证 django内置方法  from django.contrib import authenticate
        flag = authenticate(username=username,password=password)

        if flag is not None:
            # 找到了用户
            active = flag.is_active

            if active ==1:# 1 账号正确，也已经激活。
                # 1 session记住是哪个用户，【比如购物车模块还要使用到该用户信息】
                # 1 使用 from django.contrib.auth import login
                # 1 让用户的id保持到session中。 方便以后的查询。
                LOGIN(request,flag)

                # 登录进去的情况下判断是否记住用户名
                next_url = request.GET.get('next',reverse('shouye'))
                logging.warning(next_url)
                response = redirect(next_url)
                # 判断
                remeber = request.POST.get('remeber')
                if remeber == 'on':
                    # 记住用户名
                    response.set_cookie('username',username)

                else:
                    # 不要记住用户名，cookies username必须删除,不然就显示了
                    response.delete_cookie('username')

                return response


            elif active ==0:# 2 没有激活
                return render(request, 'login.html', {'errormsg': '请去邮箱激活'})
        else:
            # flag == None  没有该用户
            return render(request, 'login.html', {'errormsg': '用户不存在'})

def b(request):
    return render(request,'base_user_center.html')
@login_required
def usercenterinfo(request):
    return render(request,'user_center_info.html',{'flag':'info'})
@login_required
def usercentersite(request):
    return render(request,'user_center_site.html',{'flag':'site'})
@login_required
def usercenterorder(request):
    return render(request,'user_center_order.html',{'flag':'order'})

