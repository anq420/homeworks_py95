from django.shortcuts import render, redirect, get_object_or_404
from .models import News, Comment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from blog.forms import ArticleForm

User = get_user_model()


def main_view(request):
    all_news = News.objects.all()
    context = {'data': all_news[::-1]}

    return render(request, 'main_page.html', context)


@login_required
def add_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            image = form.cleaned_data['image']
            nickname = request.user
            news = News(title=title, content=content, author=nickname, image=image)
            news.save()
            return redirect('main')
        else:
            messages.error(request, 'Проверьте правильность введённой информации')
    else:
        form = ArticleForm()

    return render(request, 'add_article.html', {'form': form})


@login_required
def edit_article_view(request, id):
    article = get_object_or_404(News, id=id)

    if article.author != request.user:
        return redirect(f'/article_page/{article.id}/')

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.content = form.cleaned_data['content']

            if form.cleaned_data['image']:
                article.image = form.cleaned_data['image']
            article.save()

            return redirect('main')
        else:
            messages.error(request, 'Проверьте правильность введённой информации')
    else:
        form = ArticleForm(initial={
            'title': article.title,
            'content': article.content,
            'image': article.image
        })

    return render(request, 'edit_article.html', {'form': form, 'news': article})


def full_article_view(request, id):
    news = get_object_or_404(News, id=id)
    comments = Comment.objects.filter(news_id=news.id).order_by('-created_at')

    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        content = request.POST.get('content')

        if nickname and content:
            comment = Comment.objects.create(nickname=nickname, content=content, news_id=news.id)
            return redirect('article_page', id=news.id)

    context = {'news': news, 'comments': comments}
    return render(request, 'detailed_article.html', context)


def author_view(request, id):
    author = get_object_or_404(User, id=id)
    news = News.objects.filter(author_id=id)
    return render(request, 'authors_news.html', {'news': news, 'author': author})
