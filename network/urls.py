from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newpost",views.newpost,name="newpost"),
    path("profile/<str:user>",views.profile,name="profile"),
    path("follow_unfollow/<str:user>",views.follow_unfollow,name="follow_unfollow"),
    path("following",views.following,name="following"),
    path("edit",views.edit,name="edit"),
    path("like",views.like,name="like")

]
