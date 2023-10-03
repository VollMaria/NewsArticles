from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page


urlpatterns = [
   path('', NewsList.as_view(), name='news_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('search/', NewsSearch.as_view(), name='search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
   path('authors/', AuthorList.as_view(), name='authors'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe')

]
