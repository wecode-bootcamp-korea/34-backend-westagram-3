from django.urls    import path
from users.views    import SingUpView, LogInView

urlpatterns = [
    path('/users/signup', SingUpView.as_view()),
    path('/users/login', LogInView.as_view())
]