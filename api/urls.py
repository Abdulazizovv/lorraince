from django.urls import path
from api import views


urlpatterns = [
    path('users/', views.BotUserListView.as_view(), name='users-list'),
    path('users/<int:pk>/', views.BotUserDetailView.as_view(), name='users-detail'),
    path('soft-slides/', views.SoftSlideListView.as_view(), name='slides-list'),
    path('soft-slides/<int:pk>/', views.SoftSlideDetailView.as_view(), name='slides-detail'),
]