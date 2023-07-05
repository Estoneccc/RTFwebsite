from django.shortcuts import render, get_object_or_404, redirect
from .models import Article

def main_page(request):
    return render(request, 'main_page.html')

def information(request):
    return render(request, 'information.html')

def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})

def job(request):
    return render(request, 'job.html')

def add_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        article = Article(title=title, content=content)
        article.save()
        return redirect('article_detail', pk=article.pk)
    return render(request, 'add_article.html')