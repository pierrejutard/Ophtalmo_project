from django.shortcuts import render, get_object_or_404
from ophtalmo_blog.models import ophtalmo_article
from django.http import HttpResponse

def ophtalmo_article_index(request):
    ophtalmo_articles = ophtalmo_article.objects.all()
    return render(request, 'ophtalmo_blog/ophtalmo_article_index.html', context={"ophtalmo_articles":ophtalmo_articles})

def ophtalmo_article_details(request, slug):
    ophtalmo_article_detail = get_object_or_404 (ophtalmo_article, slug=slug)
    return render(request, 'ophtalmo_blog/ophtalmo_article_details.html', context={"ophtalmo_article_detail":ophtalmo_article_detail})