import bleach as bleach
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Specialization
import requests


def main_page(request):
    return render(request, 'index.html')


def information(request):
    return render(request, 'reference-info.html')


def article_list(request):
    articles = Article.objects.all()
    return render(request, 'article_list.html', {'articles': articles})


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'article_detail.html', {'article': article})


def add_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        article = Article(title=title, content=content)
        article.save()
        return redirect('article_detail', pk=article.pk)
    return render(request, 'add_article.html')


def get_vacancies_by_specialization(specialization):
    url = 'https://api.hh.ru/vacancies'
    params = {'text': specialization}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        vacancies = response.json()
        return vacancies['items']
    else:
        return None


def get_specializations():
    return Specialization.objects.all()


def employment(request):
    specializations = get_specializations()
    selected_specialization = request.GET.get('specialization', '') # Извлекаем выбранную специализацию из параметра запроса
    vacancies_list = []

    if selected_specialization: # Если выбрана специализация, получаем вакансии только для нее
        vacancies = get_vacancies_by_specialization(selected_specialization)
        if vacancies:
            for vacancy in vacancies:
                name = vacancy.get('name')
                snippet = vacancy.get('snippet')
                salary = vacancy.get('salary')
                url = vacancy.get('alternate_url')
                if snippet:
                    responsibility = bleach.clean(snippet.get('responsibility'), tags=[], strip=True)
                if salary:
                    currency = salary.get('from')
                vacancy_obj = {
                    'title': name,
                    'description': responsibility,
                    'salary': currency,
                    'url': url
                }
                vacancies_list.append(vacancy_obj)
    else: # Если не выбрана специализация, получаем все вакансии
        for specialization in specializations:
            vacancies = get_vacancies_by_specialization(specialization.name)
            if vacancies:
                for vacancy in vacancies:
                    name = vacancy.get('name')
                    snippet = vacancy.get('snippet')
                    salary = vacancy.get('salary')
                    url = vacancy.get('alternate_url')
                    if snippet:
                        responsibility = bleach.clean(snippet.get('responsibility'), tags=[], strip=True)
                    if salary:
                        currency = salary.get('from')
                    vacancy_obj = {
                        'title': name,
                        'description': responsibility,
                        'salary': currency,
                        'url': url
                    }
                    vacancies_list.append(vacancy_obj)

    context = {'vacancies': vacancies_list, 'specializations': specializations, 'selected_specialization': selected_specialization}
    return render(request, 'employment.html', context)
