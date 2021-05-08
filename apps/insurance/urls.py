from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from .views import ProfileAPI, ProfileUpdateAPI, ProfilesListAPI, MyObtainTokenPairView, InsurerRegisterAPI, ChangePasswordAPI, \
    LogoutAllAPI, LogoutAPI,InsurerAPI,RegisterAssessorAPI,EvalCaseAPI

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='login'),
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh'),
    path('register/', InsurerRegisterAPI.as_view(), name='register'),
    path('register-assessor/', RegisterAssessorAPI.as_view(), name='register_assessor'),
    path('change_password/<id>/', ChangePasswordAPI.as_view(), name='change_password'),
    path('logout/', LogoutAPI.as_view(), name='logout'),
    path('logoutall/', LogoutAllAPI.as_view(), name='logout_all'),


    path('profiles/', ProfilesListAPI.as_view(), name='profiles_list'),
    path('profile/', include([
        path('<user_id>/', ProfileAPI.as_view(), name='profile'),
        path('<user_id>/update/', ProfileUpdateAPI.as_view(), name='update_profile'),
    ])),
    path('insurer/<user_id>', InsurerAPI.as_view(), name='user_info'),
    path('create-evalcase/',EvalCaseAPI.as_view(),name='create_eval_case')
]
