from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Note(models.Model):
    title = models.CharField(verbose_name='Заголовок заметки', max_length=255)
    content = models.TextField(verbose_name='Содержание заметки', max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        db_table = 'note'

    def __str__(self) -> str:
        return self.title
