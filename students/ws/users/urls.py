from django.urls import path

from users.views import SighUpView

urlpatterns = [
    path('/signup', SighUpView.as_view()),
]