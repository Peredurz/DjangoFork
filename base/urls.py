"""
URL configuration for Apotheek project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .forms import CustomChangePasswordForm

urlpatterns = [
    path("", views.index, name="index"),
    path("", include("django.contrib.auth.urls")),
    path(
        "login/",
        views.Login,
        name="login",
    ),
    path("register/", views.register, name="register"),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path(
        "collections_for_admin/",
        views.collections_for_admin,
        name="collections_for_admin",
    ),
    path(
        "collections_for_user/", views.collections_for_user, name="collections_for_user"
    ),
    path("create_collection/", views.create_collection, name="create_collection"),
    path(
        "create_collection/<int:pk>/",
        views.create_collection,
        name="create_collection_with_medicine",
    ),
    path("delete_collection/", views.delete_collection, name="delete_collection"),
    path(
        "approve_collection/<int:pk>/",
        views.approve_collection,
        name="approve_collection",
    ),
    path(
        "approve_collected/<int:pk>/", views.approve_collected, name="approve_collected"
    ),
    path(
        "unapprove_collection/",
        views.unapproved_collection,
        name="unapproved_collections",
    ),
    path(
        "delete_collection/<int:pk>/", views.delete_collection, name="delete_collection"
    ),
    path("new_medicine/", views.new_medicine, name="new_medicine"),
    path(
        "new_medicine_confirm/<int:pk>/",
        views.new_medicine_confirm,
        name="new_medicine_confirm",
    ),
    path("medicine/", views.medicine, name="medicine"),
    path("edit_medicine/<int:pk>/", views.edit_medicine, name="edit_medicine"),
    path(
        "edit_password/done",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="base/edit_password_done.html"
        ),
        name="edit_password_done",
    ),
    path(
        "edit_password/",
        auth_views.PasswordChangeView.as_view(
            template_name="base/edit_password.html",
            form_class=CustomChangePasswordForm,
            success_url="/edit_password/done",
        ),
        name="edit_password",
    ),
    path("medicine/<int:pk>/", views.medicine_profile, name="medicine_profile"),
    path("admin_profile/<int:pk>/", views.admin_profile, name="admin_profile"),
]
