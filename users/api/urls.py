from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("me/", views.CurrentUserView.as_view(), name="me"),
    path("token/login/", views.TokenCreateView.as_view(), name="token_login"),
    path("token/logout/", views.TokenDestroyView.as_view(), name="token_logout"),
    path("create/", views.CreateUserView.as_view(), name="users_create"),
    path("list/", views.UserListView.as_view(), name="users_list"),
    path("<int:pk>/detail/", views.UserDetailView.as_view(), name="users_detail"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="users_delete"),
]
