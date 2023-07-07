from django.contrib import admin
from .models import Article, Specialization

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass

admin.site.register(Specialization)