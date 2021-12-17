from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import AccountForm, AccountRegisterForm

# Create your views here.

def user_login(request):
    if request.method == 'POST':
        login_form = AccountForm(data=request.POST)
        if login_form.is_valid():
            data = login_form.cleaned_data
            """此处注意，username和password是authenticate里要求的字段，即User类里储存的同字段"""
            user = authenticate(username=data['user_name'], password=data['user_password'])
            if user:
                """login方法一定要有这2个参数，同时不要把外面函数名起成login，会报错，就近原则会变成提示给了2个参数!!!"""
                login(request, user)
                return redirect('article:article_list')
            else:
                return HttpResponse("账号或密码有误，请重新输入。")
        else:
            return HttpResponse("账号或密码格式不正确，请重新输入。")
    elif request.method =='GET':
        login_form = AccountForm()
        context = {'from' : login_form}
        return render(request, 'login.html', context)
    else:
        return HttpResponse("请使用GET或者POST请求数据")
            
def user_logout(request):
    logout(request)
    return redirect('article:article_list')

def account_register(request):
    if request.method == 'POST':
        account_register_form = AccountRegisterForm(data=request.POST)
        if account_register_form.is_valid():
            new_account = account_register_form.save(commit=False)
            new_account.set_password(account_register_form.cleaned_data['password'])
            new_account.save()
            login(request, new_account)
            #redirect禁止空格，会导致路径出错
            return redirect('article:article_list')
        else:
            return HttpResponse("注册信息输入有误，请重新输入。")
    elif request.method == 'GET':
        account_register_form = AccountRegisterForm()
        context = {'form' : account_register_form}
        return render(request, 'register.html', context)
    else:
        return HttpResponse("请使用GET或者POST请求数据")