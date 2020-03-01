from django.contrib import admin
from .models import Post, Group

class PostAdmin(admin.ModelAdmin): # перечисляем поля, которые должны отображаться в админке
    list_display = ("pk", "text", "pub_date", "author")  # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)  # добавляем возможность фильтрации по дате
    list_filter = ("pub_date",)  
    empty_value_display = '-пусто-'  # это свойство сработает для всех колонок: где пусто - там будет эта строка
    def group_title(self, obj):
        return obj.group.title
    group_title.short_description = "Group"
    
class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "description")
    empty_value_display = '-пусто-'
    
# при регистрации модели Post источником конфигурации для неё назначаем класс PostAdmin (для отображения к админке)
admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
    