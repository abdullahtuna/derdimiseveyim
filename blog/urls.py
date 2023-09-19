from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('iletisim/', views.iletisim, name='iletisim'),
    path('kurallar/', views.kurallar, name='kurallar'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
]