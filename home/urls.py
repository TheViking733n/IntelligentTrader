from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('tnc/', views.tnc, name='tnc'),
    path('privacy/', views.privacy, name='privacy'),
    path('refund/', views.refund, name='refund'),
    path('signup/', views.signup, name='signup'),
    path('beginners-booster-course/', views.beginners_booster_course, name='beginners-booster-course'),
    path('advanced-conqueror-course/', views.advanced_conqueror_course, name='advanced-conqueror-course'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('updateprofile/', views.updateprofile, name='updateprofile'),
    path('promo/<str:course>/', views.promo, name='promo'),
    path('promo/', views.promo, name='promo'),
    path('verifypromo/', views.verifypromo, name='verifypromo'),
]
