from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ArticlePostForm
from .models import ArticlePost
from django.contrib.auth.models import User
# Create your views here.

def article_list(request):
    articles = ArticlePost.objects.all()

    context = {'articles' : articles}

    return render(request, 'list.html', context)

def article_detail(request, id):
    article = ArticlePost.objects.get(id=id)

    context = { 'article' : article}

    return render(request, 'detail.html', context)

def article_create(request):
    if request.method == 'POST':
        article_post_form = ArticlePostForm(data = request.POST)
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写.")
    else:
        article_post_form = ArticlePostForm()
        context = {'article_post_form' : article_post_form}
        return render(request, 'create.html', context)

def article_delete(request, id):
    article = ArticlePost.objects.get(id=id)
    article.delete()
    return redirect("article:article_list")

def article_safe_delete(request, id):
    if request.method == 'POST':
        article = ArticlePost.objects.get(id=id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许post请求')