from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Specialization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name