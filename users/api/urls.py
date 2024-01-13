from django.urls import path

from . import views


app_name = "users"

urlpatterns = [
    path("me/", views.CurrentUserView.as_view(), name="me"),
    path("token/login/", views.TokenCreateView.as_view(), name="token-login"),
    path("token/logout/", views.TokenDestroyView.as_view(), name="token-logout"),
    path("create/", views.CreateUserView.as_view(), name="user-create"),
    path("list/", views.UserListView.as_view(), name="user-list"),
    path("<int:pk>/detail/", views.UserDetailView.as_view(), name="user-detail"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
]
