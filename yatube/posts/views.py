from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from .models import Post, Group, User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import datetime as dt
from django.urls import reverse
from django.utils import timezone

def index(request):
    post_list = Post.objects.order_by("-pub_date").all()
    paginator = Paginator(post_list, 10) # показывать по 10 записей на странице.
# Для получения параметров из строки запроса применяется метод request.GET.get().
    page_number = request.GET.get('page') # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number) # получить записи с нужным смещением
    return render(request, 'index.html', {'page': page, 'paginator': paginator})

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:12]
    return render(request, "group.html", {"group": group, "posts": posts})

@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST) # request.post содержит данные из полей на сайте
        if form.is_valid():
            post = form.save(commit=False)  # принимаем данные от формы
            post.author = request.user
            post.save()
            return redirect(reverse('index'))
        return render(request, 'new_post.html', {'form': form}) 
    form = PostForm()            
    return render(request, "new_post.html", {"form": form})

# Basically, we have two things here: we save the form with form.save and we add an author (since there was no author field in the PostForm and this field is required). 
# commit=False means that we don't want to save the Post model yet – we want to add the author first. Most of the time you will use form.save() 
# without commit=False, but in this case, we need to supply it. post.save() will preserve changes (adding the author) and a new blog post is created! 

def profile(request, username):
    profile = get_object_or_404(User, username=username) # получаем объект User и колонку, из которой выбираем данные
    posts = Post.objects.filter(author=profile).order_by("-pub_date") # все посты одного автора по ключу\
    my_posts = Post.objects.filter(author=profile).count()
    paginator  = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "profile.html", {"profile": profile, 'page': page, 'paginator': paginator, "my_posts": my_posts})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id) # функция get_object_or_404 получает по заданным критериям объект из базы данных или возвращант сообщение об ошибке, если объект не найден \
    profile = get_object_or_404(User, username=username)
    my_posts = Post.objects.filter(author=profile).count()
    return render(request, "post.html", {"post": post, "my_posts": my_posts})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id) # мы передаём параметр pk из URL-адреса
    if request.user == post.author:
        if request.method == "POST": # Когда мы возвращаемся к представлению со всей информацией, которую мы ввели в форму.
            form = PostForm(request.POST, instance = post) # передаём экземпляр post в качестве instance форме и при сохранени
            if form.is_valid(): 
                post = form.save(commit=False)
                post.author = request.user
                post.pub_date = timezone.now()
                post.save()
                return redirect('index')
            return render(request, 'post_edit.html', {'form': form})
        form = PostForm(instance=post) # Когда мы только зашли на страницу и хотим получить пустую форму
        return render(request, "post_edit.html", {"form": form})
    return redirect("post", post_id=post_id, username=post.author.username)
