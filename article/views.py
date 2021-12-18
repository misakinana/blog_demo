from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from .models import ArticlePost
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def article_list(request):
    articles = ArticlePost.objects.all()

    context = {'articles' : articles}

    return render(request, 'list.html', context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    context = { 'article' : article}

    return render(request, 'detail.html', context)

@login_required(login_url='/account/login/')
def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写.")
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form' : article_post_form}
        return render(request, 'create.html', context)

@login_required(login_url='/account/login/')
def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

@login_required(login_url='/account/login/')
def article_safe_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你不是该文章作者或管理员，无权修改这篇文章。")
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许post请求')

@login_required(login_url='/account/login/')
def article_update(request, id):
    article = ArticlePost.objects.get(id=id)
    if request.user != article.author:
        return HttpResponse("抱歉，你不是该文章作者或管理员，无权修改这篇文章。")
    if request.method =='POST':
        article_update_form = ArticlePostForm(data=request.POST)
        if article_update_form.is_valid():
            updated_article = article_update_form.cleaned_data
            article.title = updated_article['title']
            article.body = updated_article['body']
#            article.title = request.POST['title']
#            article.body = request.POST['body']
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse("文章格式不正确，请重新修改。")
    else:
        article_update_form = ArticlePostForm()
        context = { 'article' : article, 'article_update_form' : article_update_form }
        return render(request, 'update.html', context)
            