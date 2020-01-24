from django.urls import path

from wx import views

urlpatterns = [
    path(r"test/", views.Test.as_view()),
]