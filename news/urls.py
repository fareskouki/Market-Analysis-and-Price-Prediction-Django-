from django.urls import path
from . import views



urlpatterns = [
    path('', views.news_list, name='news_list'),
    path('upload/', views.upload_and_train, name='upload_and_train'),
    path('upload-news/', views.upload_and_analyze_news, name='upload_and_analyze_news'),
    path('upload-pdf/', views.upload_and_analyze_news_pdf, name='upload_and_analyze_news_pdf'),
    path('forecast/', views.result_chart_with_forecast, name='result_chart_with_forecast'),

    # CRUD operations for NewsArticle
    path('articles/create/', views.create_article, name='create_article'),
    path('articles/update/<int:pk>/', views.update_article, name='update_article'),
    path('articles/delete/<int:pk>/', views.delete_article, name='delete_article'),
    path('articles/<int:pk>/comment/', views.add_comment, name='add_comment'),

]
