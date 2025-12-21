from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/edit/', views.ProfileEditView.as_view(), name="profile"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('signup/', views.RegisterView.as_view(), name="register"),
    path('logout/', views.logout_view, name="logout"),
    # path('', views.index, name='index'),
]
