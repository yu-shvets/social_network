from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='account-create'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh'),

    path('post_create/', views.PostCreateApiView.as_view(), name='post-create'),
    path('post/<int:pk>/like/', views.PostLikesUpdateApiView.as_view(), name='post-like'),
    path('post/<int:pk>/dislike/', views.PostDisLikesUpdateApiView.as_view(), name='post-dislike'),

    path('analytics/', views.AnalyticsAPIView.as_view(), name='analytics'),
    path('user_analytics/', views.UserAnalyticsAPIView.as_view(), name='user-analytics')
]
