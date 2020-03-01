"""yatube URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views

urlpatterns = [
    # импорт правил из приложения posts, обработчик для главной страницы 
    path("", include("posts.urls")), 
    # flatpages
    path("about/", include("django.contrib.flatpages.urls")),
    # импорт правил из приложения admin
    path("admintest/", admin.site.urls),
    # регистрация и авторизация
    path("auth/", include("users.urls")),
    # если нужного шаблона для /auth не нашлось в файле users.urls — 
    # ищем совпадения в файле django.contrib.auth.urls
    path("auth/", include("django.contrib.auth.urls")),
]
# в urls.py главного файла будут только ссылки на urls.py приложений проекта
urlpatterns += [
        path('about-us/', views.flatpage, {'url': '/about-us/'}, name='about'),
        path('terms/', views.flatpage, {'url': '/terms/'}, name='terms'),
        path('about-author/', views.flatpage, {'url': "about-author/"}, name="about-author"),
        path('about-spec/', views.flatpage,  {'url': "about-spec/"}, name="about-spec")
]
# Теперь страницы с адресами /about-us и /terms будут обрабатываться view-функцией flatpage() приложения flatpages.
# {'url': '/about-us/'} и {'url': '/license/'} — это параметры, которые path() передаёт в вызываемую view-функцию. Это даёт нам свободу: например, мы можем обработать URL
