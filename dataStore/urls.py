from django.urls import path
from .views import BlogItemViews,RegisterView,LoginView,LogoutView,BlogView

urlpatterns = [
    path('', BlogItemViews.as_view()),
    path('blogs/', BlogView.as_view()),
    path("register/",RegisterView.as_view()),
    path("login/",LoginView.as_view()),
    path("logout/",LogoutView.as_view()),
]