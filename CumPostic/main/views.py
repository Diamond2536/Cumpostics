from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Post, Comments, PostType, PostCategory
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import UserCreationForm
from django.contrib.auth.decorators import user_passes_test

def index(request):
    posts_list = Post.objects.all().prefetch_related('post_screenshots')
    paginator = Paginator(posts_list, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except:
        posts = paginator.page(paginator.num_pages)

    post_types = PostType.objects.all()
    post_categories = PostCategory.objects.all()
    return render(request, 'index.html', {'posts': posts, 'post_types': post_types, 'post_categories': post_categories})

def index_type(request, url):
    posts_list = Post.objects.filter(type__url=url)
    paginator = Paginator(posts_list, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except:
        posts = paginator.page(paginator.num_pages)

    post_types = PostType.objects.all()
    post_categories = PostCategory.objects.all()
    return render(request, 'index.html', {'posts': posts, 'post_types': post_types, 'post_categories': post_categories})

def index_category(request, url):
    posts_list = Post.objects.filter(category__url=url)
    paginator = Paginator(posts_list, 3)
    try:
        page = int(request.GET.get('page', '1'))
    except:
        page = 1

    try:
        posts = paginator.page(page)
    except:
        posts = paginator.page(paginator.num_pages)

    post_types = PostType.objects.all()
    post_categories = PostCategory.objects.all()
    return render(request, 'index.html', {'posts': posts, 'post_types': post_types, 'post_categories': post_categories})

@user_passes_test(lambda u: u.is_authenticated, login_url='/register/')
def post(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comments.objects.filter(post=post)
    if request.method == "POST":
        if request.user.is_authenticated:
            text = request.POST.get("text", False)
            new_comment = Comments(user=request.user, text=text, post=post)
            new_comment.save()
            return redirect('main:post', id=id, slug=slug)
        else:
            return HttpResponseForbidden()
    else:
        context = {
            'post': post,
            'comments': comments
        }
        return render(request, 'post.html', context)

class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('main:index'))
        context = {
            'form': form
        }
        return render(request, self.template_name, context)
