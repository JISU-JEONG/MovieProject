from django.urls import path
from . import views


app_name = "movies"
urlpatterns = [
    path('', views.index,name='index'),
    path('<int:movie_id>/', views.detail,name='detail'),
    path('<int:movie_id>/reviews/new/', views.review_new, name='review_new'),
    path('<int:movie_id>/reviews/<int:review_id>/review_delete/', views.review_delete, name='review_delete'),
    path('<int:movie_id>/like/', views.like, name='like'),
    path('<int:movie_id>/score/', views.score, name='score'),
    path('search/', views.search, name='search')
]
