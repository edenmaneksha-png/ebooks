from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('books', views.BookViewSet, basename='book')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register,    name='register'),
    path('auth/login/',    views.login_view,  name='login'),
    path('auth/logout/',   views.logout_view, name='logout'),
    path('auth/me/',       views.me,          name='me'),
    path('progress/',      views.ReadingProgressView.as_view(), name='progress'),
]
