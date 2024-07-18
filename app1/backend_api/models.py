# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     GENDERS = (
#         ('m', 'Мужчина'),
#         ('f', 'Женщина')
#     )

#     surname = models.CharField(verbose_name='Фамилия', max_length=45, default='', null=True)
#     name = models.CharField(verbose_name='Имя', max_length=45, default='', null=True)
#     patronymic = models.CharField(verbose_name='Отчество', max_length=45, default='', null=True)

#     gender = models.CharField(verbose_name='Пол', max_length=1, choices=GENDERS, default='',  null=True)
#     birth_date = models.DateField(verbose_name='Дата рождения',  null=True)

#     created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
#     updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

#     def __str__(self) -> str:
#         return self.username


# class Note(models.Model):
#     title = models.CharField(verbose_name='Заголовок заметки', max_length=255)
#     content = models.TextField(verbose_name='Содержание заметки', max_length=1000)
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
#     created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
#     updated = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

#     def __str__(self) -> str:
#         return self.title
