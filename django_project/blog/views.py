from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse
from .models import Post

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.core.paginator import Paginator

@login_required
def home(request):

    context = {'posts':Post.objects.all()}
    return render(request, 'blog/home.html', context)

@login_required
def about(request):

    context = {'title':'About'}
    return render(request, 'blog/about.html',context)

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<viewstype>.html #<blog>/<Post>_<ListView>.html
    context_object_name = 'posts'
    # ordering = ['-date_created']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<viewstype>.html #<blog>/<Post>_<ListView>.html
    context_object_name = 'posts'
    ordering = ['-date_created']
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_created')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False
        # return super().test_func()


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False


# class PostSearchView():
#     model = Post
#     fields = ['author']