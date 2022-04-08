
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.new_post, name="new_post"),
    path("user/<int:id>", views.user, name="user"),
    path("follow/<int:user_id>", views.follow, name="follow"),
    path("following", views.following, name="following"),
    path("profile",views.profile, name="profile"),
    path("edit/<int:post_id>", views.edit, name="edit"),
    path("new_heart/<int:post_id>", views.new_heart, name="new_heart"),
    path("hearts", views.heart, name="heart"),
    path("delete/<int:post_id>", views.delete, name="delete")
]
