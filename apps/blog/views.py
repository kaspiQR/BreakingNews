from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Category, News, Like


def index(request):
    news = News.objects.all()
    categories = Category.objects.all()
    index_categories = []

    for category in categories:
        item = {
            'id': category.id,
            'title': category.title,
            'link': category.slug,
            'news': News.objects.filter(category__id=category.id)
        }
        index_categories.append(item)
    context = {
        'news': news,
        'categories': categories,
        'index_categories': index_categories[:4]
    }
    return render(request, 'index.html', context=context)


def news_detail(request, pk):
    news = News.objects.get(pk=pk)
    news.views += 1
    news.save()
    news.refresh_from_db()
    context = {
        'n': news
    }
    return render(request, 'news_detail.html', context=context)


def get_news_category(request, slug):
    category_obj = Category.objects.get(slug=slug)
    news = News.objects.filter(category__slug=slug)
    # news = News.objects.filter(category=category_obj)
    # news = News.objects.filter(category__id=category_obj.id)

    context = {
        'category': category_obj,
        'news': news
    }
    return render(request, 'category.html', context=context)


def like_view(user, news):
    like = Like.objects.filter(user=user, news=news).exists()
    if not like:
        like = Like.objects.create(user=user, news=news)
        like.save()
    else:
        Like.objects.get(user=user, news=news).delete()


def news_like(request, news_id):
    news = News.objects.get(id=news_id)
    user = request.user
    if user.is_authenticated:
        like_view(user=user, news=news)
        return redirect('/')

    news = News.objects.all()
    categories = Category.objects.all()
    index_categories = []
    for category in categories:
        item = {
            'id': category.id,
            'title': category.title,
            'link': category.slug,
            'news': News.objects.filter(category__id=category.id),

        }
        index_categories.append(item)
    context = {
        'news': news,
        'categories': categories,
        'index_categories': index_categories[:4],
        'message': 'Что бы поставить лайк Регистрируйтесь или Авторизуйтесь'
    }
    return render(request, 'index.html', context=context)


def news_like_detail(request, news_id):
    news = News.objects.get(id=news_id)
    user = request.user
    if user.is_authenticated:
        like_view(user=user, news=news)
        return render(request, 'news_detail.html', context={
            'n': news
        })

    return render(request, 'news_detail.html', context={
        'n': news,
        'message': 'Что бы поставить лайк Регистрируйтесь или Авторизуйтесь'
    })


def search(request):
    q = request.GET.get('s')
    news = News.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
    context = {'news': news}
    return render(request, 'category.html', context=context)
