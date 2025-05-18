from django.urls import path
from . import views

    
urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.loginPage, name='login'),
    path('signup/', views.signup, name = 'signup'),
    path('challenges/', views.challenges, name='challenges'),
    path('about/', views.about, name='about'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('logout/', views.logoutUser, name='logout'),
    path('challenges/<slug:slug>/', views.category_detail, name='category'),
    path('<str:category_name>/<str:challenge_title>/', views.challenge_details, name='challenge_details'),
    path('api/submit/<int:challenge_id>/', views.submit_flag, name='submit_flag'),
    path('api/hint/unlock/<int:hint_id>/<int:challenge_id>', views.unlock_hint, name='unlock_hint'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
]
