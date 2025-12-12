
    # myapp/urls.py
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Register_Page, name="register"),
    path('login/', views.Login_Page, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('home/', views.Home_Page, name="home"),
    path('shift/<str:pk>', views.shift_page, name="shift"),
    path('end_shift/<str:pk>', views.end_shift, name="end_shift"),
    path('shift/<int:pk>/add_downtime/', views.add_downtime, name="add_downtime"),
    ]
