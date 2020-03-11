from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .forms import PostForm, CommentForm
from .models import Post, Group, User, Comment, Follow
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import datetime as dt
from django.urls import reverse
from django.views.decorators.cache import cache_page

@cache_page(20)
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
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page, 'paginator': paginator})


@login_required
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST,  files=request.FILES or None) # request.post содержит данные из полей на сайте
        if form.is_valid():
            post = form.save(commit=False)  # принимаем данные от формы
            post.author = request.user
            post.save()
            return redirect(reverse('index'))
        return render(request, 'new_post.html', {'form': form}) # если is_valid = False
    form = PostForm()  # пустая форма       
    return render(request, "new_post.html", {"form": form})

# Basically, we have two things here: we save the form with form.save and we add an author (since there was no author field in the PostForm and this field is required). 
# commit=False means that we don't want to save the Post model yet – we want to add the author first. Most of the time you will use form.save() 
# without commit=False, but in this case, we need to supply it. post.save() will preserve changes (adding the author) and a new blog post is created! 

def profile(request, username):
    profile = get_object_or_404(User, username=username) # получаем объект User и колонку, из которой выбираем данные
    posts = Post.objects.filter(author=profile).order_by("-pub_date").all() # все посты одного автора по ключу
    my_posts = Post.objects.filter(author=profile).count()
    paginator  = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    followers = Follow.objects.filter(author=profile).count() # количество подписчиков
    followed = Follow.objects.filter(user=profile).count() # количество подписок
    following = Follow.objects.filter(user=request.user.id, author=profile) # if following
    return render(request, "profile.html", {"profile": profile, 'page': page, 'paginator': paginator, "my_posts": my_posts, "followers": followers, "followed": followed, "following": following})


def post_view(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id) # функция get_object_or_404 получает по заданным критериям объект из базы данных или возвращант сообщение об ошибке, если объект не найден \
    profile = get_object_or_404(User, username=username)
    my_posts = Post.objects.filter(author=profile).count()
    comments = Comment.objects.filter(post=post).order_by('-created')
    form = CommentForm()
    return render(request, "post.html", {"form": form, "post": post, "my_posts": my_posts, "profile": profile, "comments": comments})


@login_required
def post_edit(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id) # мы передаём параметр pk из URL-адреса
    user = get_object_or_404(User, username=username)
    if request.user != user:
        return redirect("post", post_id=post_id, username=request.user.username)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post) # форма со старыми и новыми данными
    if request.method == "POST":
        if form.is_valid(): 
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect ('post', username=request.user.username, post_id=post_id)  
    return render(request, "post_edit.html", {"form": form, "post": post})

@login_required
def add_comment(request, username, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect("post", username=request.user.username, post_id=post_id)
    return render(request, "comments.html", {"form": form, "post": post})

@login_required
def follow_index(request):
    followed = Follow.objects.filter(user=request.user) # на каких авторов подписан пользователь
    authors = []
    for author in followed:
        authors.append(author.author.id) # экземляр модели User (= User.id)
    posts = Post.objects.filter(author__in=authors).order_by("-pub_date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    return render(request, "follow.html", {"paginator": paginator, "page": page})


@login_required
def profile_follow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follow_check = Follow.objects.filter(user=user, author=author).exists()
    if not follow_check and author != user:
        Follow.objects.create(user=request.user, author=author)
    return redirect("profile", username=username)


@login_required
def profile_unfollow(request, username):
    user = request.user
    author = get_object_or_404(User, username=username)
    follow_check = Follow.objects.filter(user=user, author=author).exists()
    if follow_check:
        Follow.objects.filter(user=user, author=author).delete()
    return redirect("profile", username=username)


def page_not_found(request, exception=None):
    # Переменная exception содержит отладочную информацию, 
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(request, "misc/404.html", {"path": request.path}, status=404)

def server_error(request):
    return render(request, "misc/500.html", status=500)
