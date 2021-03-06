from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("post/submit", views.post_submit, name="post_submit"),
    path("post/<int:post_id>", views.post, name="post"),
    path("user/<str:username>", views.user_profile, name="user_profile"),
    path("user/<str:username>/follow", views.follow, name="follow"),
    path("user/<str:username>/unfollow", views.unfollow, name="unfollow"),
    path("following", views.following, name="following")
]
