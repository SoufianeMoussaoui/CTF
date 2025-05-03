from django.urls import path
from . import views

    
urlpatterns = [
    path('', views.home, name = 'home'),
    path('login/', views.loginPage, name='login'),
    path('signup/', views.signup, name = 'signup'),
    path('challenges/', views.challenges, name='challenges'),
    path('about/', views.about, name='about'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('dashboard/', views.dashboardPage, name='dashboard'),
    path('logout/', views.logoutUser, name='logout'),
    
    path('<slug:slug>/', views.category_detail, name='category'),
    path('api/challenge/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),
    path('api/submit/<int:challenge_id>/', views.submit_flag, name='submit_flag'),
    path('api/hint/unlock/<int:hint_id>/', views.unlock_hint, name='unlock_hint'),
]