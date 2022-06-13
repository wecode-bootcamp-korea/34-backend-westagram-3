from django.urls    import path
from users.views    import SingUpView

urlpatterns = [
    path('/signup', SingUpView.as_view())
] 