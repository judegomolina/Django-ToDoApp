from django.urls import path

from .views import SignUpView, UserEditView

urlpatterns = [
    path('signup', SignUpView.as_view(), name='signup'),
    path('profile', UserEditView.as_view(), name='user_profile'),
]