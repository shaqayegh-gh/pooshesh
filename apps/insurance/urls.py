from django.urls import path, include
from .views import RegisterAPI, LoginAPI, ProfileAPI,ProfileUpdateAPI,ProfilesListAPI,UpdatePasswordView
from knox import views as knox_views

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('updatepassword/', UpdatePasswordView.as_view(), name='update_password'),

    path('profiles/', ProfilesListAPI.as_view(), name='profiles_list'),
    path('profile/', include([
        path('<user_id>/', ProfileAPI.as_view(), name='profile'),
        path('<user_id>/update/', ProfileUpdateAPI.as_view(), name='update_profile'),
    ])),
]
