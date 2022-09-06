from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('', views.sign_in, name="sign_in"),
    # path('home/', views.home, name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password/<slug:token>/', views.reset_password, name="reset_password"),
    path('change_password/', views.change_password, name="change_password"),


    #From here start with education
    path('edu_create/',views.create_post, name="edu_create"),
    path('home/',views.list_post, name="home"),
    path('edu_dlt/<pk>/',views.delete_post, name="edu_dlt"),



]
