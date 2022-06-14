from django.urls import path
from users.views import SingUpView, LogInView

urlpatterns = [
    path('/signup', SingUpView.as_view()),
    path('/login', LogInView.as_view())
] 