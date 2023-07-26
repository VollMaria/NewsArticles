from django.urls import path
from .views import NewsList, PostDetail, multiply, NewsSearch, NewsCreate, ArticlesCreate, NewsEdit, ArticleEdit, NewsDelete, ArticleDelete


urlpatterns = [
   path('', NewsList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('multiply/', multiply),
   path('search/', NewsSearch.as_view(), name='search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('articles/create/', ArticlesCreate.as_view(), name='article_create'),
   path('news/<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
   path('articles/<int:pk>/edit/', ArticleEdit.as_view(), name='article_edit'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete')

]
