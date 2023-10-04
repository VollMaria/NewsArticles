from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_protect
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import *
from django.http import HttpResponse
from .filters import PostFilter
from .forms import NewsForm
from django.core.cache import cache
import logging
from django.utils.translation import gettext as _

logger = logging.getLogger(__name__)


def index(request):
    logger.info('INFO')
    news = Post.objects.all()
    return render(request, 'news.html', context={'news': news})


class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    template_name = 'authors.html'


class NewsList(ListView):
    model = Post
    ordering = '-creation_time'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'new.html'
    context_object_name = 'new'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'new-{self.kwargs["pk"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'new-{self.kwargs["pk"]}', obj)
        return obj


def multiply(request):
    number = request.GET.get('number')
    multiplier = request.GET.get('multiplier')

    try:
        result = int(number) * int(multiplier)
        html = f"<html><body>{number}*{multiplier}={result}</body></html>"
    except (ValueError, TypeError):
        html = f"<html><body>Invalid input.</body></html>"

    return HttpResponse(html)


class NewsSearch(ListView):
    model = Post
    ordering = '-creation_time'
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        if self.request.path == '/news/news/create/':
            post.categoryType = 'NW'
        post.save()
        return super().form_valid(form)


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'news_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('articles.add_post',)
    raise_exception = True
    form_class = NewsForm
    model = Post
    template_name = 'art_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'AR'
        if self.request.path == '/news/articles/create/':
            post.categoryType = 'AR'
        post.save()
        return super().form_valid(form)


class ArticleEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('articles.change_post',)
    form_class = NewsForm
    model = Post
    template_name = 'art_edit.html'


class ArticleDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('articles.delete_post',)
    model = Post
    template_name = 'art_delete.html'
    success_url = reverse_lazy('news_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by('-creation_time')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required
@csrf_protect
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы оформили подписку на категорию'
    return render(request, 'subscribe.html', {'category': category, 'message': message})

@login_required
@csrf_protect
def unsubscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.remove(user)

    message = 'Вы успешно отписались от рассылки новостей категории '
    return render(request, 'unsubscribe.html', {'category': category, 'message': message})


class Index(View):
    def get(self, request):
        string = _('Hello world')
        return HttpResponse(string)