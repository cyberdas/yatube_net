from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model() # для работы с пользователями


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.title 

class Post(models.Model): # класс Post, наследник класса Model из библиотеки models
    text = models.TextField() # свойство pub_date типа DateTimeField, текст "date published" это заголовок
    pub_date = models.DateTimeField("date published", auto_now_add=True) # поля в интерфейсе администратора. auto_now_add говорит, что при создании новой записи автоматически будет подставлено текущее время и дата 
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, blank=True, null=True, related_name="posts")

    def __str__(self): # выводим текст поста  
        return self.text 
# Параметр on_delete=models.CASCADE обеспечивает связность данных: если из таблицы User будет удалён пользователь, то будут удалены все связанные с ним посты.
# будет создана таблица с этими ячейками
